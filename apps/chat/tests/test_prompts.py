from apps.chat.prompts import get_intro_message


def test_get_intro_message_formats_correctly():
    topic = "Convince me the Earth is flat"
    expected = (
        'The topic is: "Convince me the Earth is flat".\n'
        "You are defending that position.\n"
        "Your goal is to convince the opponent that you are right.\n"
    )

    result = get_intro_message(topic)

    assert result == expected
