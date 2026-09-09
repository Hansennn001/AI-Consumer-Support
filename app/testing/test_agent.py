from app.testing.assessment_cases import (


    test_security_breach,

    test_data_loss,

    test_service_outage,

    test_customer_history,

    test_refund_rag,

    test_tool_decision,

    test_memory

)



def run_test(name, test_function):

    print("\n==============================")
    print(name)
    print("==============================")


    try:

        result = test_function()


        print("STATUS: PASS")


        print("\nOUTPUT:")

        print(
            "Category:",
            result.get("category")
        )


        print(
            "Risk:",
            result.get("risk_level")
        )


        print(
            "Risk Reason:",
            result.get("risk_reason")
        )


        print(
            "Human:",
            result.get("requires_human")
        )


        print(
            "Tool:",
            result.get("use_tool")
        )


        print(
            "Tool Name:",
            result.get("tool_name")
        )


        print(
            "Status:",
            result.get("status")
        )


        print(
            "Response:",
            result.get("response")
        )


        return True



    except AssertionError as e:


        print("STATUS: FAIL")

        print(
            "Assertion Error:",
            e
        )

        return False



    except Exception as e:


        print("STATUS: ERROR")

        print(e)

        return False





def main():


    tests = [

        (
            "1. Security Breach Escalation",
            test_security_breach
        ),


        (
            "2. Data Loss Escalation",
            test_data_loss
        ),


        (
            "3. Service Outage Escalation",
            test_service_outage
        ),


        (
            "4. Customer Contact >3 Times / 7 Days",
            test_customer_history
        ),


        (
            "5. Refund Knowledge Base",
            test_refund_rag
        ),


        (
            "6. Realtime Tool Decision",
            test_tool_decision
        ),


        (
            "7. Conversation Memory",
            test_memory
        )

    ]


    passed = 0



    print(
        """
========================================
POINTSTAR AGENT VALIDATION
========================================
"""
    )



    for name, test in tests:


        if run_test(name, test):

            passed += 1



    print(
        f"""
========================================
FINAL RESULT

{passed}/{len(tests)} TEST PASSED

========================================
"""
    )




if __name__ == "__main__":

    main()