import datetime
import os
import uuid
#파일이 업로드 될 때 파일을 올린 날짜별로 폴더로 나누어 구성
def file_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    d = datetime.datetiem.now()
    filepath = d.strftime("%Y/%m/%d")
    suffix = d.strftime("%Y%m%d%H%M%S")
    filename = "%s_%s.%s" % (uuid.uuid4().hex, suffix, ext)
    return os.path.join(filepath,filename)