from subprocess import check_output, CalledProcessError


class Ping(object):

    def __init__(self, host="8.8.8.8"):
        self.host = host
    
    def get_ping(self):
        try:
            raw_response = check_output(['ping', self.host, '-n', '1'], universal_newlines=True)
            response = "".join(raw_response).replace("<", "=").split("=")
        except CalledProcessError:
            response = "time-out"
        return response
