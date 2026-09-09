from app.state.agent_state import AgentState
from app.database.db import save_memory

import logging
import json


logger = logging.getLogger(__name__)



def save_conversation(state: AgentState):

    try:

        # =====================================
        # Validate assistant response
        # SQLite hanya menerima tipe sederhana:
        # string, integer, float, None
        # =====================================

        response = state.get(
            "response",
            ""
        )


        if not isinstance(
            response,
            str
        ):

            logger.warning(
                "Response is not string. Converting to JSON string."
            )


            state["response"] = json.dumps(
                response,
                ensure_ascii=False
            )



        # =====================================
        # Save conversation memory
        # =====================================

        save_memory(state)


        logger.info(
            "Conversation memory saved successfully"
        )



    except Exception as e:


        # Memory failure tidak boleh
        # menghentikan customer response

        logger.error(
            "Failed to save conversation memory",
            exc_info=True
        )



    return state