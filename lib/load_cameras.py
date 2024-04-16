from flask_restx import Resource
import logging
import requests
import traceback

from .api import api
from .config import config
from .exceptions import NotFoundError
data_ = json.loads((r'{"mode":"start","mid":"10998","name":"ReoLinkWireless","type":"h264","protocol":"rtsp",'
                   r'"host":"192.168.1.40","port":"554","path":"/","ext":"mp4","fps":"3","width":"2048","height":"1536",'
                   r'"details":"{\"notes\":\"\",\"dir\":\"\",\"auto_host_enable\":\"1\",'
                   r'\"auto_host\":\"rtsp://user:pass@192.168.1.40:554/\",\"rtsp_transport\":\"tcp\",\"muser\":\"user\",'
                   r'\"mpass\":\"pass\",\"port_force\":null,\"fatal_max\":\"0\",\"aduration\":\"1000000\",'
                   r'\"probesize\":\"1000000\",\"stream_loop\":null,\"sfps\":\"\",\"accelerator\":\"0\",\"hwaccel\":\"cuvid\",'
                   r'\"hwaccel_vcodec\":\"h264_cuvid\",\"hwaccel_device\":\"\",\"stream_type\":\"mp4\",'
                   r'\"stream_flv_type\":\"http\",\"stream_flv_maxLatency\":\"\",\"stream_mjpeg_clients\":\"0\",'
                   r'\"stream_vcodec\":\"copy\",\"stream_acodec\":\"no\",\"hls_time\":\"2\",\"hls_list_size\":\"2\",'
                   r'\"preset_stream\":\"\",\"signal_check\":\"\",\"signal_check_log\":\"0\",\"stream_quality\":\"1\",'
                   r'\"stream_fps\":\"10\",\"stream_scale_x\":\"3072\",\"stream_scale_y\":\"1728\",\"rotate_stream\":null,'
                   r'\"svf\":\"\",\"tv_channel\":null,\"tv_channel_id\":\"\",\"tv_channel_group_title\":\"\",'
                   r'\"stream_timestamp\":null,\"stream_timestamp_font\":\"\",\"stream_timestamp_font_size\":\"\",'
                   r'\"stream_timestamp_color\":\"\",\"stream_timestamp_box_color\":\"\",\"stream_timestamp_x\":\"\",'
                   r'\"stream_timestamp_y\":\"\",\"stream_watermark\":\"0\",\"stream_watermark_location\":\"\",'
                   r'\"stream_watermark_position\":null,\"snap\":\"0\",\"snap_fps\":\"1\",\"snap_scale_x\":\"1920\",'
                   r'\"snap_scale_y\":\"1072\",\"snap_vf\":\"\",\"vcodec\":\"copy\",\"crf\":\"1\",\"preset_record\":\"\",'
                   r'\"acodec\":\"no\",\"dqf\":\"0\",\"cutoff\":\"\",\"rotate_record\":null,\"vf\":\"\",\"timestamp\":\"0\",'
                   r'\"timestamp_font\":\"\",\"timestamp_font_size\":\"\",\"timestamp_color\":\"\",'
                   r'\"timestamp_box_color\":\"\",\"timestamp_x\":\"\",\"timestamp_y\":\"\",\"watermark\":null,'
                   r'\"watermark_location\":\"\",\"watermark_position\":null,\"cust_input\":\"\",\"cust_snap\":\"\",'
                   r'\"cust_rtmp\":\"\",\"cust_rawh264\":\"\",\"cust_detect\":\"\",\"cust_stream\":\"\",'
                   r'\"cust_stream_server\":\"\",\"cust_record\":\"\",\"custom_output\":\"\",\"detector\":\"0\",'
                   r'\"detector_pam\":\"0\",\"detector_noise_filter\":null,\"detector_webhook\":\"0\",'
                   r'\"detector_webhook_url\":\"\",\"detector_command_enable\":\"0\",\"detector_command\":\"\",'
                   r'\"detector_command_timeout\":\"\",\"detector_lock_timeout\":\"\",\"detector_save\":\"0\",'
                   r'\"detector_frame_save\":\"0\",\"detector_mail\":\"0\",\"detector_mail_timeout\":\"\",'
                   r'\"detector_record_method\":\"sip\",\"detector_trigger\":\"1\",\"detector_trigger_record_fps\":\"\",'
                   r'\"detector_timeout\":\"10\",\"watchdog_reset\":\"0\",\"detector_delete_motionless_videos\":\"0\",'
                   r'\"detector_send_frames\":\"1\",\"detector_region_of_interest\":\"0\",\"detector_fps\":\"\",'
                   r'\"detector_scale_x\":\"640\",\"detector_scale_y\":\"480\",\"detector_use_motion\":\"1\",'
                   r'\"detector_use_detect_object\":\"0\",\"detector_frame\":\"0\",\"detector_sensitivity\":\"\",\"cords\":\"['
                   r']\",\"detector_buffer_vcodec\":\"auto\",\"detector_buffer_fps\":\"\",\"detector_buffer_hls_time\":\"\",'
                   r'\"detector_buffer_hls_list_size\":\"\",\"detector_buffer_start_number\":\"\",'
                   r'\"detector_buffer_live_start_index\":\"\",\"detector_lisence_plate\":\"0\",'
                   r'\"detector_lisence_plate_country\":\"us\",\"detector_notrigger\":\"0\",\"detector_notrigger_mail\":\"0\",'
                   r'\"detector_notrigger_timeout\":\"\",\"control\":\"0\",\"control_base_url\":\"\",'
                   r'\"control_url_method\":null,\"control_stop\":null,\"control_url_stop_timeout\":\"\",'
                   r'\"control_url_center\":\"\",\"control_url_left\":\"\",\"control_url_left_stop\":\"\",'
                   r'\"control_url_right\":\"\",\"control_url_right_stop\":\"\",\"control_url_up\":\"\",'
                   r'\"control_url_up_stop\":\"\",\"control_url_down\":\"\",\"control_url_down_stop\":\"\",'
                   r'\"control_url_enable_nv\":\"\",\"control_url_disable_nv\":\"\",\"control_url_zoom_out\":\"\",'
                   r'\"control_url_zoom_out_stop\":\"\",\"control_url_zoom_in\":\"\",\"control_url_zoom_in_stop\":\"\",'
                   r'\"groups\":\"\",\"loglevel\":\"quiet\",\"sqllog\":\"0\",\"detector_cascades\":\"\",'
                   r'\"stream_channels\":\"\",\"input_maps\":\"\",\"input_map_choices\":\"\"}","shto":"[]","shfr":"[]"}'))
details_ = json.loads(data_['details'])
cur_route = api.namespace("load_cameras", description="load cameras by room", path="/load_cameras/")

@cur_route.route("/<string:room>")
class LoadCamerasViaConfig(Resource):
    """
    Load cameras in shinobi
    """

    def _get_request_url(self, settings):
        data = copy.copy(data_)
        details = copy.copy(details_)

        ip = ""
        for index, char in enumerate(settings['ip']):
            if char.isdigit() or char == "." or (char == ":" and settings['ip'][index + 1].isdigit()):
                ip += char
        if "https" in settings["ip"]:
            settings["ip"] = f"https://{ip}"
        else:
            settings["ip"] = f"http://{ip}"

        for key, value in settings.items():
            if key in data and value is not None:
                data[key] = value
            if key in details and value is not None:
                details[key] = value

        details_string = str(details)
        details_string = details_string.replace("'", r'\"')
        details_string = details_string.replace(" ", "")
        details_string = details_string.replace("None", "null")
        del data['details']

        data_string = str(data)
        data_string = f"{data_string[:-1]}, 'details': '{details_string}'"
        data_string = data_string.replace("'", '"') + "}"

        url = f"{settings['ip']}/{settings['api']}/configureMonitor/{settings['group_key']}/{settings['mid']}/?data={data_string}"
        return url
    def _load_cameras(self, room):
        if room in config._data["rooms"].camerasByRoom:
            for camera in config._data["rooms"].camerasByRoom[room]:
                settings = {"ip": config._data["shinobi_url"],
                            "api": config._data["api_key"],
                            "group_key": config._data["group_key"],
                            "mid": camera["mid"],
                            "auto_host": camera["auto_host"]}
                try:
                    request_url_base_path = _get_request_url(settings)
                    response = requests.post(url, verify=False, timeout=60)
                    return True
                except NotFoundError:
                    raise
                except Exception as e:
                    logging.error(traceback.format_exc())
                    return False
        else:
            raise NotFoundError(f"room {room} not presented in config")

    def post(self, room):
        return {"ok": self._load_cameras(room)}
