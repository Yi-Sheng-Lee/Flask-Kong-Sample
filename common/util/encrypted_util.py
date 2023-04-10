from cryptography.fernet import Fernet


def getDecodeCode_test(decode_data_name):
    # decode_data_name 欲解密之binary檔案 example : sqlcode , rediscode
    # return 解密後明文

    # 讀取金鑰
    with open("./common/util/public.bin", 'rb') as f:
        key = f.read()

    cipher_suite = Fernet(key.decode("utf-8"))

    # 讀取加密資料
    with open("./common/util/" + decode_data_name + ".bin", "rb") as f:
        decodeKey = f.read()
        f.close()

    # 輸出解密後的資料
    data = cipher_suite.decrypt(decodeKey, None)
    decodeCode = data.decode("utf-8")

    return decodeCode


def encodeData_test(encode_data_name, encode_text):
    # 欲加密文字轉 bytes
    data = bytes(encode_text, 'utf-8')

    # 判別如果是 redis 就直接讀 key 檔案
    # 否則 建立一把 key 並寫入 public.bin 內
    if encode_data_name == 'rediscode':
        with open('./common/util/public.bin', "rb") as f:
            key = f.read()
        cipher_suite = Fernet(key)
    else:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)

        with open('./common/util/public.bin', "wb") as f:
            f.write(key)

    cipher_msg = cipher_suite.encrypt(data)

    with open("./common/util/" + encode_data_name + ".bin", "wb") as f:
        f.write(cipher_msg)
