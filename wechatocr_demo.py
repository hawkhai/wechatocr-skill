#encoding=utf8
import re, os, sys
import time, json
import subprocess
import requests

def writefile(path, data, encoding="ISO8859-1", force=False):
    assert type(encoding) == type(""), encoding
    if type(data) == type(""):
        data = data.encode(encoding)
    dir = os.path.dirname(path)
    if dir and not os.path.exists(dir):
        os.makedirs(dir)

    fout = open(path, "wb") # writefile
    fout.write(data)
    fout.close()
    return True

def find_wechatocr_serv():
    work_dir = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(work_dir, "wechatocr", "wechatocr_serv.exe")

def is_wechatocr_serv_running():
    output = subprocess.check_output(["tasklist", "/FI", "IMAGENAME eq wechatocr_serv.exe"], encoding="gbk", errors="ignore")
    return "wechatocr_serv.exe" in output

def ensure_wechatocr_serv_running():
    if not is_wechatocr_serv_running():
        serv_path = find_wechatocr_serv()
        print(f"[wechatocr] wechatocr_serv.exe not running, starting: {serv_path}")
        subprocess.Popen([serv_path], cwd=os.path.dirname(serv_path))
        time.sleep(2)
    else:
        print("[wechatocr] wechatocr_serv.exe already running")

def find_model():
    wechatocrfile = "wechatocr_1-7079.infz"
    work_dir = os.path.split(os.path.abspath(__file__))[0]
    wechatocrinfz = os.path.join(work_dir, "wechatocr", wechatocrfile)
    return os.path.abspath(wechatocrinfz)

def wechatocr_netget(fpath, force=False):

    fdir, fname = os.path.split(fpath)
    ftype = os.path.splitext(fname)[-1]
    if not ftype.lower() in (".jpg", ".jpeg", ".png", ".bmp"):
        return None

    fnamec = os.path.splitext(fname)[0]
    jsonfile = os.path.join(fdir, fnamec+"_wechatocr.json")
    if not force and os.path.exists(jsonfile):
        return jsonfile

    message = {
        "imgfile": os.path.abspath(fpath),
    }
    wechatocrinfz = find_model()
    if os.path.exists(wechatocrinfz):
        message["wechatocrfile"] = os.path.abspath(wechatocrinfz)

    reqdata = {
        "message": json.dumps(message),
        "name": "wechatocr",
    }
    reqdata = json.dumps(reqdata).encode("utf8")
    print(reqdata)
    ensure_wechatocr_serv_running()
    response = requests.get("http://127.0.0.1:8811/Infai/Echo", data=reqdata)
    fdata = response.json()

    result = json.dumps(json.loads(fdata["message"]))
    print(result)
    writefile(jsonfile, result, encoding="utf8")
    return jsonfile

if __name__ == "__main__":
    wechatocr_netget("test.png", True)
    #main(r"F:\pythonx\myocr\doclayout\样本图片")
    print("ok")
