from app.key_manager import API_KEYS
from langchain_google_genai import ChatGoogleGenerativeAI



class GeminiFallback:


    def __init__(self):

        self.keys = API_KEYS



    def invoke(self, prompt):

        last_error = None


        for key in self.keys:

            try:

                llm = ChatGoogleGenerativeAI(

                    model="gemini-3.6-flash",

                    google_api_key=key,

                    temperature=0.2

                )


                response = llm.invoke(prompt)


                print(
                    "Success with key:",
                    key[:10]
                )


                return response


            except Exception as e:

                print(
                    "Failed key:",
                    key[:10]
                )

                last_error = e



        raise Exception(
            f"No Gemini key available: {last_error}"
        )