import datetime
import warnings
from pathlib import Path
from typing import Union

import numpy as np
from nptdms import ChannelObject, GroupObject, RootObject, TdmsFile, TdmsWriter
from sdypy_sep005 import Sep005Data


def read_tdms(path: Union[str, Path]) -> list[Sep005Data]:  # noqa: UP007
    """Primary function to read tdms files based on the path.

    .. code-block:: python
        signals = dw.readTDMS(path)

    Returns an empty list when file failed

    :param path: path to a .tdms file
    """

    if not Path(path).is_file():
        warnings.warn(
            f"FAILED IMPORT: No TDMS file at: {path}", UserWarning, stacklevel=2
        )
        return []

    try:
        tdms_file = TdmsFile(path)
    except FileNotFoundError:
        warnings.warn(
            f"FAILED IMPORT: No TDMS file at: {path}", UserWarning, stacklevel=2
        )
        return []
    except ValueError:
        warnings.warn(
            f"FAILED IMPORT: TDMS file at: {path} seems corrupted."
            " Failed to import.",
            UserWarning,
            stacklevel=2,
        )
        return []

    signals = []
    groups = tdms_file.groups()

    for group in groups:
        channels = tdms_file[group.name].channels()
        for channel in channels:
            signal = {
                "group": group.name,
                "name": str(channel).split("/")[2][1:-2],
            }
            if "unit_string" in channel.properties:
                unit_str = channel.properties["unit_string"]
            else:
                unit_str = ""
            signal["unit_str"] = unit_str
            signal["data"] = tdms_file[group.name][channel.name].data
            signal["fs"] = 1 / channel.properties["wf_increment"]
            if "wf_start_time" in channel.properties:
                signal["start_timestamp"] = np.datetime_as_string(
                    channel.properties["wf_start_time"], unit="s"
                )
            signals.append(signal)

    return [Sep005Data.model_validate(signal) for signal in signals]


def write_tdms(
    signals: Union[list[Sep005Data], list[dict], Sep005Data, dict],  # noqa: UP007
    path: Union[str, Path],  # noqa: UP007
    author: str = "sdypy_io_tdms",
    timestamp=None,
):
    """Write a SEP005 formatted object into a TDMS file"""
    if not isinstance(signals, list):
        signals = [signals]  # Convert single instance to a list

    signals_converted: list[Sep005Data] = list(signals)
    for index, signal in enumerate(signals):
        if isinstance(signal, dict):
            signals_converted[index] = Sep005Data.model_validate(signal)

    if timestamp is None:
        for signal in signals_converted:
            if signal.start_timestamp is not None:
                timestamp = datetime.datetime.fromisoformat(
                    signal.start_timestamp
                )

        if timestamp is None:
            timestamp = datetime.datetime.now(datetime.timezone.utc)  # noqa: UP017

    root_object = RootObject(
        properties={
            "author": author,
            "datestring": timestamp.strftime("%Y/%m/%d H:%M:%S"),
        }
    )

    with TdmsWriter(path, "w") as tdms_writer:
        tdms_writer.write_segment([root_object])
        for signal in signals_converted:
            if signal.group is None:
                raise ValueError(
                    "signal.group attribute should not be None as it is"
                    " required for a TDMS file"
                )
            group_object = GroupObject(signal.group)
            channel_object = ChannelObject(
                signal.group,
                signal.name,
                np.array(signal.data, dtype="float32"),
                properties={
                    "unit_string": signal.unit_str,
                    "wf_increment": 1 / signal.fs,
                },
            )
            tdms_writer.write_segment([group_object, channel_object])
