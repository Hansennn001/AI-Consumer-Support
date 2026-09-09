from langchain_google_genai import ChatGoogleGenerativeAI

from app.key_manager import API_KEYS



class GeminiFallback:


    def __init__(self):

        self.keys = API_KEYS



    def invoke(self, prompt):


        last_error = None


        for key in self.keys:


            try:

                print(
                    "Using Gemini key:",
                    key[:10]
                )


                llm = ChatGoogleGenerativeAI(

                    model="gemini-3.6-flash",

                    google_api_key=key,

                    temperature=0.2,

                    max_retries=0

                )


                response = llm.invoke(prompt)


                return response



            except Exception as e:


                print(
                    "Failed key:",
                    key[:10]
                )


                print(e)


                last_error = e



        raise last_error





def get_llm_with_fallback():

    return GeminiFallback()