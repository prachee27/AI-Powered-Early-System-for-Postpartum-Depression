TOTAL_EPDS_QUESTIONS = 10

LOW_RISK_MAX = 9
MODERATE_RISK_MAX = 12


EPDS_CONFIG = {

    1: {
        "question": "I have been able to laugh and see the funny side of things",
        "options": [
            "As much as I always could",
            "Not quite so much now",
            "Definitely not so much now",
            "Not at all"
        ],
        "score_map": {
            0: 0,
            1: 1,
            2: 2,
            3: 3
        }
    },

    2: {
        "question": "I have looked forward with enjoyment to things",
        "options": [
            "As much as I ever did",
            "Rather less than I used to",
            "Definitely less than I used to",
            "Hardly at all"
        ],
        "score_map": {
            0: 0,
            1: 1,
            2: 2,
            3: 3
        }
    },

    3: {
        "question": "I have blamed myself unnecessarily when things went wrong",
        "options": [
            "Yes, most of the time",
            "Yes, some of the time",
            "Not very often",
            "No, never"
        ],
        "score_map": {
            0: 3,
            1: 2,
            2: 1,
            3: 0
        }
    },

    4: {
        "question": "I have been anxious or worried for no good reason",
        "options": [
            "No, not at all",
            "Hardly ever",
            "Yes, sometimes",
            "Yes, very often"
        ],
        "score_map": {
            0: 0,
            1: 1,
            2: 2,
            3: 3
        }
    },

    5: {
        "question": "I have felt scared or panicky for no very good reason",
        "options": [
            "Yes, quite a lot",
            "Yes, sometimes",
            "No, not much",
            "No, not at all"
        ],
        "score_map": {
            0: 3,
            1: 2,
            2: 1,
            3: 0
        }
    },

    6: {
        "question": "Things have been getting on top of me",
        "options": [
            "Yes, most of the time I haven't been able to cope at all",
            "Yes, sometimes I haven't been coping as well as usual",
            "No, most of the time I have coped quite well",
            "No, I have been coping as well as ever"
        ],
        "score_map": {
            0: 3,
            1: 2,
            2: 1,
            3: 0
        }
    },

    7: {
        "question": "I have been so unhappy that I have had difficulty sleeping",
        "options": [
            "Yes, most of the time",
            "Yes, sometimes",
            "Not very often",
            "No, not at all"
        ],
        "score_map": {
            0: 3,
            1: 2,
            2: 1,
            3: 0
        }
    },

    8: {
        "question": "I have felt sad or miserable",
        "options": [
            "Yes, most of the time",
            "Yes, quite often",
            "Not very often",
            "No, not at all"
        ],
        "score_map": {
            0: 3,
            1: 2,
            2: 1,
            3: 0
        }
    },

    9: {
        "question": "I have been so unhappy that I have been crying",
        "options": [
            "Yes, most of the time",
            "Yes, quite often",
            "Only occasionally",
            "No, never"
        ],
        "score_map": {
            0: 3,
            1: 2,
            2: 1,
            3: 0
        }
    },

    10: {
        "question": "The thought of harming myself has occurred to me",
        "options": [
            "Yes, quite often",
            "Sometimes",
            "Hardly ever",
            "Never"
        ],
        "score_map": {
            0: 3,
            1: 2,
            2: 1,
            3: 0
        }
    }

}