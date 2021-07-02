import logging
import os
"""Custom logger to log on console """
logging.basicConfig(
        format="%(asctime)s : %(levelname)s : [%(filename)s:%(lineno)s - %(funcName)10s()] : %(message)s"
  )
poster = logging.getLogger("poster")
poster.setLevel(os.getenv("LOGLEVEL", logging.DEBUG))