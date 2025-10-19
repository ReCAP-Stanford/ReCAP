
def get_few_shot():
    return [
        {
            "role": "user",
            "content": """Observation:
Station table1:
table1 is a table
table1 has bread1
table1 has bread1 directly on top of it
table1 has no players at it

Station board1:
board1 is a cutting board
board1 has lettuce1
board1 has lettuce1 directly on top of it
board1 has no players at it

Station sink1:
sink1 is a sink
sink1 has nothing on it
sink1 has no players at it

Station stove1:
stove1 is a stove
stove1 is occupied by robot1
stove1 has bread2
stove1 has bread2 directly on top of it

Station fryer1:
fryer1 is a fryer
fryer1 has onion1
fryer1 has onion1 directly on top of it
fryer1 has no players at it

Station table2:
table2 is a table
table2 has nothing on it
table2 has no players at it

Station board2:
board2 is a cutting board
board2 has bottombun1
board2 has bottombun1 directly on top of it
board2 has no players at it

Station table3:
table3 is a table
table3 has nothing on it
table3 has no players at it

Station sink2:
sink2 is a sink
sink2 has potato1
sink2 has potato1 directly on top of it
sink2 has no players at it

Station sink3:
sink3 is a sink
sink3 has cheese1
sink3 has cheese1 directly on top of it
sink3 has no players at it

Station sink4:
sink4 is a sink
sink4 has onion2
sink4 has onion2 directly on top of it
sink4 has no players at it

Station fryer2:
fryer2 is a fryer
fryer2 has nothing on it
fryer2 has no players at it

Item bread1:
bread1 is a bread slice
bread1 is at table1
bread1 is directly on top of table1
bread1 has nothing above it

Item lettuce1:
lettuce1 is a head of lettuce
lettuce1 can be cut on a cutting board
lettuce1 is at board1
lettuce1 is directly on top of board1
lettuce1 has nothing above it

Item bread2:
bread2 is a bread slice
bread2 is at stove1
bread2 is directly on top of stove1
bread2 has nothing above it

Item onion1:
onion1 is an onion
onion1 can be cut on a cutting board
onion1 is at fryer1
onion1 is directly on top of fryer1
onion1 has nothing above it

Item bottombun1:
bottombun1 is a bottom bun
bottombun1 is at board2
bottombun1 is directly on top of board2
bottombun1 has nothing above it

Item potato1:
potato1 is a potato
potato1 is at sink2
potato1 is directly on top of sink2
potato1 has nothing above it

Item cheese1:
cheese1 is a cheese slice
cheese1 is at sink3
cheese1 is directly on top of sink3
cheese1 has nothing above it

Item onion2:
onion2 is an onion
onion2 can be cut on a cutting board
onion2 is at sink4
onion2 is directly on top of sink4
onion2 has nothing above it

Item tomato1:
tomato1 is a tomato
tomato1 can be cut on a cutting board
tomato1 is held by robot1

Player robot1:
robot1 is a robot
robot1 is at stove1
robot1 is holding tomato1

Valid Actions:
Move robot1 from stove1 to table1
Move robot1 from stove1 to board1
Move robot1 from stove1 to sink1
Move robot1 from stove1 to fryer1
Move robot1 from stove1 to table2
Move robot1 from stove1 to board2
Move robot1 from stove1 to table3
Move robot1 from stove1 to sink2
Move robot1 from stove1 to sink3
Move robot1 from stove1 to sink4
Move robot1 from stove1 to fryer2
Stack tomato1 on top of bread2 using robot1
Do nothing

Your current task: Prepare a onion cheese sandwich on a table

We wish you to generate a list of subtasks for the current task. Return a json object to generate your subtasks with the following structure:

{
    "think": "",  // str: Your thought
    "subtasks": [...]  // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to prepare a onion cheese sandwich on a table. I need ingredients stacked from bottom to top: table -> bread -> onion -> cheese -> bread. I am holding tomato1, but the task does not need tomato1. I have to first place it on a station to operate other items. table3 is a good choice. I need to then locate a bread as the base, cut an onion and stack it on the base bread, stack a cheese on the cut onion, and finally stack another bread on the cheese.",
    "subtasks": [
        "put tomato1 on table3",
        "locate a bread as the base",
        "cut an onion and stack it on the base bread",
        "stack a cheese on the cut onion",
        "stack another bread on the cheese"
    ]
}"""
        },
        {
            "role": "user",
            "content": """The following interactions are omitted for task put tomato1 on table3"""
        },
        {
            "role": "assistant",
            "content": """The following interactions are omitted for task put tomato1 on table3. Assume that by the end of this task, the assistant has completed this task successfully."""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: put tomato1 on table3

Now, you return to the previous stage.
Your current task: Prepare a onion cheese sandwich on a table

Your previous think: The task is to prepare a onion cheese sandwich on a table. I need ingredients stacked from bottom to top: table -> bread -> onion -> cheese -> bread. I am holding tomato1, but the task does not need tomato1. I have to first place it on a station to operate other items. table3 is a good choice. I need to then locate a bread as the base, cut an onion and stack it on the base bread, stack a cheese on the cut onion, and finally stack another bread on the cheese.

Your remaining subtasks: [
    "locate a bread as the base",
    "cut an onion and stack it on the base bread",
    "stack a cheese on the cut onion",
    "stack another bread on the cheese"
]

We wish you to refine your list of subtasks. Do not generate any subtasks beyond the scope of the current task. Return a json object to generate your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to prepare a onion cheese sandwich on a table. I need ingredients stacked from bottom to top: table -> bread -> onion -> cheese -> bread. I already placed tomato1 on a station. I need to now locate a bread as the base, cut an onion and stack it on the base bread, stack a cheese on the cut onion, and finally stack another bread on the cheese.",
    "subtasks": [
        "locate a bread as the base",
        "cut an onion and stack it on the base bread",
        "stack a cheese on the cut onion",
        "stack another bread on the cheese"
    ]
}"""
        },
        {
            "role": "user",
            "content": """Ok.

Your current task: locate a bread as the base.

We wish you to generate a list of subtasks for the current task. Return a json object to generate your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to locate a bread as the base. I see bread1 on table1 and bread2 on stove2. Since bread1 is on top of a table, it will serve as the base of the sandwich. So I don't need to do anything.",
    "subtasks": []
}"""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: locate a bread as the base

Observation:
...(omitted)...

Valid Actions:
...(omitted)...

Now, you return to the previous stage.
Your current task: Prepare a onion cheese sandwich on a table.

Your previous think: The task is to make an onion cheese sandwich on a table. I need ingredients stacked from bottom to top: table -> bread -> onion -> cheese -> bread. I need to first locate a bread as the base, then cut an onion and stack it on the base bread, then stack a cheese on the cut onion, and finally stack another bread on the cheese.

Your remaining subtasks: [
    "cut an onion and stack it on the base bread",
    "stack a cheese on the cut onion",
    "stack another bread on the cheese"
]

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to make an onion cheese sandwich on a table. I need ingredients stacked from bottom to top: table -> bread -> onion -> cheese -> bread. The base bread is set. Now I need to cut an onion and stack it on the base bread, then stack a cheese on the cut onion, and finally stack another bread on the cheese.",
    "subtasks": [
        "cut an onion and stack it on bread1 located at table1",
        "stack a cheese on the cut onion",
        "stack another bread on the cheese"
    ]
}"""
        },
        {
            "role": "user",
            "content": """Ok.

Your current task: cut an onion and stack it on bread1 located at table1

We wish you to generate a list of subtasks for the current task. Return a json object to generate your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to cut an onion and stack it on bread1 located at table1. I see onion1 on fryer1 and onion2 on sink4. I must cut an onion fully before I can stack it on top of bread1. onion1 and onion2 can be cut on a cutting board. I see board1 has lettuce1 on it and board2 has bottombun1 on it. The board must be empty before I can cut onion1 on it. I will move robot1 from stove1 to board1. I expect that by the end of the task, we will have table -> bread1 -> cut onion1",
    "subtasks": [
        "move robot1 from stove1 to board1",
        "remove lettuce1 from board1",
        "place onion1 on board1",
        "cut onion1 into rings on board1",
        "stack onion slices on bread1"
    ]
}"""
        },
        {
            "role": "user",
            "content": """Ok.

Your current task: move robot1 from stove1 to board1

We wish you to generate a list of subtasks for the current task. Return a json object to generate your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task move robot1 from stove1 to board1 can be executed directly from valid actions.",
    "subtasks": ["Move robot1 from stove1 to board1"]
}"""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: move robot1 from stove1 to board1

Observation:
...(omitted)...

Valid Actions:
...(omitted)...

Now, you return to the previous stage.
Your current task: cut an onion and stack it on bread1 located at table1

Your previous think: "The task is to cut an onion and stack it on bread1 located at table1. I see onion1 on fryer1 and onion2 on sink4. I must cut an onion fully before I can stack it on top of bread1. onion1 and onion2 can be cut on a cutting board. I see board1 has lettuce1 on it and board2 has bottombun1 on it. The board must be empty before I can cut onion1 on it. I will move robot1 from stove1 to board1. I expect that by the end of the task, we will have table -> bread1 -> cut onion1"

Your remaining subtasks: [
    "remove lettuce1 from board1",
    "place onion1 on board1",
    "cut onion1 into rings on board1",
    "stack onion slices on bread1"
]

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to cut an onion and stack it on bread1 located at table1. I see onion1 on fryer1 and onion2 on sink4. I must cut an onion fully before I can stack it on top of bread1. onion1 and onion2 can be cut on a cutting board. I see board1 has lettuce1 on it and board2 has bottombun1 on it. The board must be empty before I can cut onion1 on it. Since robot1 is at board1, I will pick up lettuce1 from board1 using robot1 and move it elsewhere. After that, I will place onion1 on board1, slice it into rings, and then stack those rings on bread1. I expect that by the end of the task, we will have table -> bread1 -> cut onion1",
    "subtasks": [
        "remove lettuce1 from board1",
        "place onion1 on board1",
        "cut onion1 into rings on board1",
        "stack onion slices on bread1"
    ]
}"""
        },
        {
            "role": "user",
            "content": """Ok.

Your current task: remove lettuce1 from board1

We wish you to generate a list of subtasks for the current task. Return a json object to generate your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to remove lettuce1 from board1. From the observation I know I am already at board1, so I will pick up lettuce1 and put it elsewhere, as long as it is not where onion1 is located or board1. table3 has tomato1 on it, but I do not need tomato1 for the task, so I will move lettuce1 to table3.",
    "subtasks": [
        "pick up lettuce1 from board1",
        "move robot1 to table3",
        "put lettuce1 on table3"
    ]
}"""
        },
        {
            "role": "user",
            "content": """Ok.

Your current task: pick up lettuce1 from board1

We wish you to generate a list of subtasks for the current task. Return a json object to update your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task pick up lettuce1 from board1 can be executed directly from valid actions",
    "subtasks": ["Pick up lettuce1 from board1 using robot1"]
}"""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: pick up lettuce1 from board1

Observation:
...(omitted)...

Valid Actions:
...(omitted)...

Now, you return to the previous stage.
Your current task: remove lettuce1 from board1

Your previous think: The task is to remove lettuce1 from board1. From the observation I know I am already at board1, so I will pick up lettuce1 and put it elsewhere, as long as it is not where onion1 is located or board1. table3 has tomato1 on it, but I do not need tomato1 for the task, so I will move lettuce1 to table3.

Your remaining subtasks: [
    "move robot1 to table3",
    "put lettuce1 on table3"
]

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to remove lettuce1 from board1. I have successfully picked up lettuce1, next I will move robot1 to table3 and put lettuce1 on table3.",
    "subtasks": [
        "move robot1 to table3",
        "put lettuce1 on table3"
    ]
}"""
        },
        {
            "role": "user",
            "content": """Ok.

Your current task: move robot1 to table3

We wish you to generate a list of subtasks for the current task. Return a json object to update your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task move robot1 to table3 can be executed directly from valid actions",
    "subtasks": ["Move robot1 from board1 to table3"]
}"""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: move robot1 to table3

Observation:
...(omitted)...

Valid Actions:
...(omitted)...

Now, you return to the previous stage.
Your current task: remove lettuce1 from board1

Your previous think: The task is to remove lettuce1 from board1. I have successfully picked up lettuce1, next I will move robot1 to table3 and put lettuce1 on table3.

Your remaining subtasks: [
    "put lettuce1 on table3"
]

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to remove lettuce1 from board1. I have successfully picked up lettuce1 and moved to table3. Next I will put lettuce1 on table3 to complete the task.",
    "subtasks": [
        "put lettuce1 on table3"
    ]
}"""
        },
        {
            "role": "user",
            "content": """Ok.

Your current task: put lettuce1 on table3

We wish you to generate a list of subtasks for the current task. Return a json object to update your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task put lettuce1 on table3 can be executed directly from valid actions",
    "subtasks": ["Place lettuce1 on table3 using robot1"]
}"""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: put lettuce1 on table3

Observation:
...(omitted)...

Valid Actions:
...(omitted)...

Now, you return to the previous stage.
Your current task: remove lettuce1 from board1

Your previous think: The task is to remove lettuce1 from board1. I have successfully picked up lettuce1 and moved to table3. Next I will put lettuce1 on table3 to complete the task.

Your remaining subtasks: []

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task remove lettuce1 from board1 is done.",
    "subtasks": []
}"""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: remove lettuce1 from board1

Now, you return to the previous stage.
Your current task: cut an onion and stack it on bread1 located at table1

Your previous think: The task is to cut an onion and stack it on bread1 located at table1. I see onion1 on fryer1 and onion2 on sink4. I must cut an onion fully before I can stack it on top of bread1. onion1 and onion2 can be cut on a cutting board. I see board1 has lettuce1 on it and board2 has bottombun1 on it. The board must be empty before I can cut onion1 on it. I will move robot1 from stove1 to board1. I expect that by the end of the task, we will have table -> bread1 -> cut onion1

Your remaining subtasks: [
    "place onion1 on board1",
    "cut onion1 into rings on board1",
    "stack onion slices on bread1"
]

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to cut an onion and stack it on bread1 located at table1. I see onion1 on fryer1 and onion2 on sink4. I must cut an onion fully before I can stack it on top of bread1. onion1 and onion2 can be cut on a cutting board. board1 has has nothing on it, so I will move onion1 to board1, cut it, and then stack cut onion1 on bread1. I expect that by the end of the task, we will have table -> bread1 -> cut onion1",
    "subtasks": [
        "move onion1 from fryer1 to board1",
        "cut onion1 into rings on board1",
        "stack onion slices on bread1"
    ]
}"""
        },
        {
            "role": "user",
            "content": """The following interactions are omitted for task move onion1 from fryer1 to board1"""
        },
        {
            "role": "assistant",
            "content": """The following interactions are omitted for task cut an onion and stack it on the base bread. Assume that by the end of this task, the assistant has completed this task successfully."""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: move onion1 from fryer1 to board1

Now, you return to the previous stage.
Your current task: cut an onion and stack it on bread1 located at table1

Your previous think: The task is to cut an onion and stack it on bread1 located at table1. I see onion1 on fryer1 and onion2 on sink4. I must cut an onion fully before I can stack it on top of bread1. onion1 and onion2 can be cut on a cutting board. board1 has has nothing on it, so I will move onion1 to board1, cut it, and then stack cut onion1 on bread1. I expect that by the end of the task, we will have table -> bread1 -> cut onion1

Your remaining subtasks: [
    "cut onion1 into rings on board1",
    "stack cut onion1 on bread1"
]

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to cut an onion and stack it on bread1 located at table1. I see onion1 is already on board1. I must cut an onion fully before I can stack it on top of bread1. Since robot1 is at board1, I will cut onion1 three times. After that, I will stack cut onion1 on bread1. I expect that by the end of the task, we will have table -> bread1 -> cut onion1",
    "subtasks": [
        "cut onion1 three times on board1",
        "stack cut onion1 on bread1"
    ]
}"""
        },
        {
            "role": "user",
            "content": """Ok.

Your current task: cut onion1 three times on board1

We wish you to generate a list of subtasks for the current task. Return a json object to update your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to cut onion1 three times on board1. I will perfom cut onion1 three times to complete the task.",
    "subtasks": [
        "cut onion1 on board1",
        "cut onion1 on board1",
        "cut onion1 on board1"
    ]
}"""
        },
        {
            "role": "user",
            "content": """The following interactions are omitted for task cut onion1 on board1"""
        },
        {
            "role": "assistant",
            "content": """The following interactions are omitted for task cut onion1 on board1. Assume that by the end of this task, the assistant has completed this task successfully."""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: cut onion1 on board1

Observation:
...(omitted)...

Valid Actions:
...(omitted)...

Now, you return to the previous stage.
Your current task: cut onion1 three times on board1

Your previous think: The task is to cut onion1 three times on board1. I will perfom cut onion1 three times to complete the task.

Your remaining subtasks: [
    "cut onion1 on board1",
    "cut onion1 on board1"
]

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to cut onion1 three times on board1. I already cut onion1 one time, I still need to cut onion1 two times to complete the task.",
    "subtasks": [
        "cut onion1 on board1",
        "cut onion1 on board1"
    ]
}"""
        },
        {
            "role": "user",
            "content": """The following interactions are omitted for task cut onion1 on board1"""
        },
        {
            "role": "assistant",
            "content": """The following interactions are omitted for task cut onion1 on board1. Assume that by the end of this task, the assistant has completed this task successfully."""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: cut onion1 on board1

Observation:
...(omitted)...

Valid Actions:
...(omitted)...

Now, you return to the previous stage.
Your current task: cut onion1 three times on board1

Your previous think: The task is to cut onion1 three times on board1. I already cut onion1 one time, I still need to cut onion1 two times to complete the task.

Your remaining subtasks: [
    "cut onion1 on board1"
]

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to cut onion1 three times on board1. I already cut onion1 two times, I still need to cut onion1 one time to complete the task.",
    "subtasks": [
        "cut onion1 on board1"
    ]
}"""
        },
        {
            "role": "user",
            "content": """The following interactions are omitted for task cut onion1 on board1"""
        },
        {
            "role": "assistant",
            "content": """The following interactions are omitted for task cut onion1 on board1. Assume that by the end of this task, the assistant has completed this task successfully."""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: cut onion1 on board1

Observation:
...(omitted)...

Valid Actions:
...(omitted)...

Now, you return to the previous stage.
Your current task: cut onion1 three times on board1

Your previous think: The task is to cut onion1 three times on board1. I already cut onion1 two times, I still need to cut onion1 one time to complete the task.

Your remaining subtasks: []

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task cut onion1 three times on board1 is done",
    "subtasks": []
}"""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: cut onion1 three times on board1

Now, you return to the previous stage.
Your current task: cut an onion and stack it on bread1 located at table1

Your previous think: The task is to cut an onion and stack it on bread1 located at table1. I see onion1 is already on board1. I must cut an onion fully before I can stack it on top of bread1. Since robot1 is at board1, I will cut onion1 three times. After that, I will stack cut onion1 on bread1. I expect that by the end of the task, we will have table -> bread1 -> cut onion1

Your remaining subtasks: [
    "stack cut onion1 on bread1"
]

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to cut an onion and stack it on bread1 located at table1. I see onion1 is already fully cut on board1. Next, I will pick up cut onion1, move to table1 and stack the cut onion1 on bread1. I expect that by the end of the task, we will have table -> bread1 -> cut onion1",
    "subtasks": [
        "pick up cut onion1",
        "move to table1",
        "stack cut onion1 on bread1",
    ]
}"""
        },
        {
            "role": "user",
            "content": """The following interactions are omitted for task cut an onion and stack it on bread1 located at table1"""
        },
        {
            "role": "assistant",
            "content": """The following interactions are omitted for task cut an onion and stack it on bread1 located at table1. Assume that by the end of this task, the assistant has completed this task successfully with table -> bread1 -> cut onion1"""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: cut an onion and stack it on bread1 located at table1

Now, you return to the previous stage.
Your current task: Prepare a onion cheese sandwich on a table

Your previous think: The task is to make an onion cheese sandwich on a table. I need ingredients stacked from bottom to top: table -> bread -> onion -> cheese -> bread. The base bread is set. Now I need to cut an onion and stack it on the base bread, then stack a cheese on the cut onion, and finally stack another bread on the cheese.

Your remaining subtasks: [
    "stack a cheese on the cut onion",
    "stack another bread on the cheese"
]

We wish you to refine your list of subtasks. Return a json object to update your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to make an onion cheese sandwich on a table. I need ingredients stacked from bottom to top: table -> bread -> onion -> cheese -> bread. The base bread is set, and onion1 is stacked on bread1. Now I need to stack a cheese on cut onion1, and finally stack another bread on the cheese.",
    "subtasks": [
        "stack a cheese on the cut onion at table1",
        "stack another bread on the cheese"
    ]
}"""
        },
        {
            "role": "user",
            "content": """The following interactions are omitted for task stack a cheese on the cut onion at table1"""
        },
        {
            "role": "assistant",
            "content": """The following interactions are omitted for task stack a cheese on the cut onion at table1. Assume that by the end of this task, the assistant has completed this task successfully with table -> bread1 -> cut onion1 -> cheese1"""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: stack a cheese on the cut onion at table1

Now, you return to the previous stage.
Your current task: Prepare a onion cheese sandwich on a table

Your previous think: The task is to make an onion cheese sandwich on a table. I need ingredients stacked from bottom to top: table -> bread -> onion -> cheese -> bread. The base bread is set, and onion1 is stacked on bread1. Now I need to stack a cheese on cut onion1, and finally stack another bread on the cheese.

Your remaining subtasks: [
    "stack another bread on the cheese"
]

We wish you to refine your list of subtasks. Return a json object to update your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task is to make an onion cheese sandwich on a table. I need ingredients stacked from bottom to top: table -> bread -> onion -> cheese -> bread. The base bread is set, onion1 is stacked on bread1, and cheese1 is stacked on onion1. Now I need to stack another bread on cheese1.",
    "subtasks": [
        "stack another bread on the cheese1 at table1"
    ]
}"""
        },
        {
            "role": "user",
            "content": """The following interactions are omitted for task stack another bread on the cheese1 at table1"""
        },
        {
            "role": "assistant",
            "content": """The following interactions are omitted for task stack another bread on the cheese1 at table1. Assume that by the end of this task, the assistant has completed this task successfully with table -> bread1 -> cut onion1-> cheese1 -> bread"""
        },
        {
            "role": "user",
            "content": """You have successfully completed the task: stack another bread on the cheese1 at table1

Now, you return to the previous stage.
Your current task: Prepare a onion cheese sandwich on a table

Your previous think: The task is to make an onion cheese sandwich on a table. I need ingredients stacked from bottom to top: table -> bread -> onion -> cheese -> bread. The base bread is set, and onion1 is stacked on bread1. Now I need to stack a cheese on cut onion1, and finally stack another bread on the cheese.

Your remaining subtasks: []

We wish you to refine your list of subtasks. Return a json object to update your subtasks with the following structure:

{
    "think": "", // str: Your thought
    "subtasks": [...] // List[str]: The updated subtask list for completing the task. If your current task can be executed directly from valid actions, the list should include only that action. If the task is done, i.e. no remaining subtasks, the updated subtask list should be empty.
}"""
        },
        {
            "role": "assistant",
            "content": """{
    "think": "The task prepare a onion cheese sandwich on a table is done.",
    "subtasks": []
}"""
        }
    ]