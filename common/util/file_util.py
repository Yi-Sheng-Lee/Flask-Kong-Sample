from common.enum.regulation_enum import ClauseError
import logging
import os

logger = logging.getLogger(__name__)

allow_type = [".pdf",".zip",".rar",".gif",".jpg",".jpeg"
             ,".png",".bmp",".txt",".doc",".docx",".ppt"
             ,".pptx",".xls",".xlsx",".7z",".key",".odt"
             ,".odp",".ods",".csv",".pages",".numbers"]


class FileManager():

    def create_file(file, target_path, save_name):
        if not FileManager.is_folder_exist(target_path):
            FileManager.create_folder(target_path)
        saved_path = os.path.join(target_path, save_name)
        file.save(saved_path)

    def delete_file(file_path, file_name):
        if FileManager.is_file_exist(file_path, file_name):
            os.remove(file_path + file_name)
        return FileManager.is_file_exist(file_path, file_name)

    def is_file_exist(file_path, file_name):
        if os.path.isfile(file_path + file_name):
            logger.info(file_path + file_name + "is exist")
            return True
        else:
            return False

    def create_folder(newpath):
        if not os.path.exists(newpath):
            os.makedirs(newpath, mode=0o777)
        return newpath

    def delete_folder(file_path):
        if os.path.exists(file_path):
            os.path.delete(file_path)

    def is_folder_exist(file_path):
        return os.path.isdir(file_path)

    def count_size(file_path, file_name):
        filesize = os.path.getsize(file_path + file_name)
        if filesize <= 1024.0:
            return str(filesize) + "bytes"
        elif (float(filesize) / float(1024)) <= 1024.0:
            return format(float(filesize) / float(1024), '.2f') + "kb"
        elif (float(filesize) / float(1024 * 1024)) <= 10.0:
            return format(float(filesize) / float(1024 * 1024), '.2f') + "Mb"
        else:
            raise Exception(ClauseError.MAXSIZE_ERROR.value)

    def get_file_name(filename):
        file_path = os.path.splitext(filename)[0]
        file_name = file_path.split('/')[-1]
        return file_name

    def get_extension(filename):
        arr = os.path.splitext(filename)
        return arr[len(arr) - 1]

    def file_filter(file_type):
        for type in allow_type:
            if type == file_type:
                return True

        return False
