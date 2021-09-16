import logging
from sys import stdout

def create_logger(name:str="LOG", file:str=None, console:bool=True, level:str="DEBUG"):
	logger = logging.getLogger(name)
	logger.setLevel(level)

	datetimeFormat = '%Y%m%d.%H%M%S'
	logFormat = ' %(asctime)s.%(msecs)03d | %(name)s | %(filename)s:%(lineno)d | %(module)s.%(funcName)s | %(levelname)-8.8s | %(message)s'
	logFormatter = logging.Formatter(logFormat, datefmt=datetimeFormat)

	if console:
		console_log_handler = logging.StreamHandler(stdout)
		console_log_handler.setFormatter(logFormatter)
		logger.addHandler(console_log_handler)

	if file:
		logFile = "logtest.py.log"
		file_log_handler = logging.FileHandler(logFile)
		file_log_handler.setFormatter(logFormatter)
		logger.addHandler(file_log_handler)

	return logger

