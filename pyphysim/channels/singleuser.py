#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module containing single user channels. """

import math
import numpy as np

from pyphysim.channels import fading, fading_generators


class SuSisoChannel(object):
    """
    Single User channel corresponding to a Tapped Delay Line channel model,
    which corresponds to a multipath channel. You can use a single tap in
    order to get a flat fading channel.

    You can create a new SuSisoChannel object either specifying the channel
    profile or specifying both the channel tap powers and delays. If only the
    fading_generator is specified then a single tap with unitary power and
    delay zero will be assumed, which corresponds to a flat fading channel
    model.

    Parameters
    ----------
    fading_generator : Subclass of FadingSampleGenerator (optional)
        The instance of a fading generator in the `fading_generators`
        module.  It should be a subclass of FadingSampleGenerator. The
        fading generator will be used to generate the channel samples. If
        not provided then RayleighSampleGenerator will be ised
    channel_profile : TdlChannelProfile
        The channel profile, which specifies the tap powers and delays.
    tap_powers_dB : numpy real array
        The powers of each tap (in dB). Dimension: `L x 1`
        Note: The power of each tap will be a negative number (in dB).
    tap_delays : numpy real array
        The delay of each tap (in seconds). Dimension: `L x 1`
    """
    def __init__(self, fading_generator=None, channel_profile=None,
                 tap_powers_dB=None, tap_delays=None, Ts=None):
        if fading_generator is None:
            fading_generator = fading_generators.RayleighSampleGenerator()
            if channel_profile is None and Ts is None:
                Ts = 1

        if (channel_profile is None and
                tap_powers_dB is None and
                tap_delays is None):
            # Only the fading generator was provided. Let's assume a flat
            # fading channel
            self._tdlchannel = fading.TdlChannel(fading_generator,
                                                 tap_powers_dB=np.zeros(1),
                                                 tap_delays=np.zeros(1),
                                                 Ts=Ts)
        else:
            # More parameters were provided. We will have then a TDL channel
            # model. Let's iust pass these parameters to the base class.
            self._tdlchannel = fading.TdlChannel(
                fading_generator,
                channel_profile, tap_powers_dB, tap_delays,
                Ts)

        # Path loss which will be multiplied by the impulse response when
        # corrupt_data is called
        self._pathloss_value = None

    def set_pathloss(self, pathloss_value=None):
        """
        Set the path loss (IN LINEAR SCALE) from each transmitter to each
        receiver.

        The path loss will be accounted when calling the corrupt_data
        method.

        If you want to disable the path loss, set `pathloss_value` to
        None.

        Parameters
        ----------
        pathloss_value : float
            The path loss (IN LINEAR SCALE) from the transmitter to the
            receiver. If you want to disable the path loss then set it to
            None.

        Notes
        -----
        Note that path loss is a power relation, which means that the
        channel coefficients will be multiplied by the square root of
        elements in `pathloss_value`.
        """
        if pathloss_value is not None:
            if pathloss_value < 0 or pathloss_value > 1:
                raise ValueError("Pathloss must be between 0 and 1")

        self._pathloss_value = pathloss_value

    def corrupt_data(self, signal):
        """
        Transmit the signal through the TDL channel.

        Parameters
        ----------
        signal : numpy array
            The signal to be transmitted.

        Returns
        -------
        numpy array
            The received signal after transmission through the TDL channel.
        """
        # output = super(SuSisoChannel, self).corrupt_data(signal)
        output = self._tdlchannel.corrupt_data(signal)

        if self._pathloss_value is not None:
            output *= math.sqrt(self._pathloss_value)

        return output

    def corrupt_data_in_freq_domain(self, signal, fft_size,
                                    carrier_indexes=None):
        """
        Transmit the signal through the TDL channel, but in the frequency
        domain.

        This is ROUGHLY equivalent to modulating `signal` with OFDM using
        `fft_size` subcarriers, transmitting through a regular TdlChannel,
        and then demodulating with OFDM to recover the received signal.

        One important difference is that here the channel is considered
        constant during the transmission of `fft_size` elements in
        `signal`, and then it is varied by the equivalent of the variation
        for that number of elements. That is, the channel is block static.

        Parameters
        ----------
        signal : numpy array
            The signal to be transmitted.
        fft_size : int
            The size of the Fourier transform to get the frequency response.
        carrier_indexes : slice of numpy array of integers
            The indexes of the subcarriers where signal is to be
            transmitted. If it is None assume all subcarriers will be used.

        Returns
        -------
        numpy array
            The received signal after transmission through the TDL channel
        """
        output = self._tdlchannel.corrupt_data_in_freq_domain(
            signal, fft_size, carrier_indexes)

        if self._pathloss_value is not None:
            output *= math.sqrt(self._pathloss_value)
        return output

    def get_last_impulse_response(self):
        """
        Get the last generated impulse response.

        A new impulse response is generated when the method `corrupt_data`
        is called. You can use the `get_last_impulse_response` method to
        get the impulse response used to corrupt the last data.

        Returns
        -------
        TdlImpulseResponse
            The impulse response of the channel that was used to corrupt
            the last data.
        """
        if self._pathloss_value is None:
            return self._tdlchannel.get_last_impulse_response()
        else:
            return math.sqrt(self._pathloss_value) * \
                self._tdlchannel.get_last_impulse_response()

    @property
    def num_taps(self):
        """Get the number of taps in the profile."""
        return self._tdlchannel.num_taps

    @property
    def num_taps_with_padding(self):
        """
        Get the number of taps in the profile including zero-padding when the
        profile is discretized.

        If the profile is not discretized an exception is raised.
        """
        return self._tdlchannel.num_taps_with_padding

    @property
    def channel_profile(self):
        """
        Return the channel profile.
        """
        return self._tdlchannel.channel_profile
