from app.database.db import save_log

import logging
import json


logger = logging.getLogger(__name__)



def log_conversation(state):

    try:

        response = state.get(
            "response",
            ""
        )


        if not isinstance(
            response,
            str
        ):

            state["response"] = json.dumps(
                response,
                ensure_ascii=False
            )


        save_log(state)


        logger.info(
            "Conversation logged successfully"
        )


    except Exception:


        logger.error(
            "Failed to save conversation log",
            exc_info=True
        )


    return state