async def add_sample_data():
    # Core Ideas (no parent)
    id1 = await add_node("Project Alpha - Initial Brainstorm")
    id2 = await add_node("Personal Development Goals")
    id3 = await add_node("Research Topics for Next Quarter")

    # Project Alpha Details
    id1_1 = await add_node("Scope Definition", parent_id=id1, position=1)
    id1_2 = await add_node("Resource Allocation", parent_id=id1, position=2)
    id1_3 = await add_node("Timeline and Milestones", parent_id=id1, position=3)

    # Scope Definition Sub-points
    id1_1_1 = await add_node("Identify Core Features", parent_id=id1_1, position=1)
    id1_1_2 = await add_node("User Stories Workshop", parent_id=id1_1, position=2)
    id1_1_3 = await add_node("Market Analysis Review", parent_id=id1_1, position=3)

    # Resource Allocation Sub-points
    id1_2_1 = await add_node("Budget Planning", parent_id=id1_2, position=1)
    id1_2_2 = await add_node("Team Assignment", parent_id=id1_2, position=2)
    id1_2_3 = await add_node("Tooling and Software", parent_id=id1_2, position=3)

    # Timeline and Milestones Sub-points
    id1_3_1 = await add_node("Phase 1: Research", parent_id=id1_3, position=1)
    id1_3_2 = await add_node("Phase 2: Development", parent_id=id1_3, position=2)
    id1_3_3 = await add_node("Phase 3: Testing", parent_id=id1_3, position=3)
    id1_3_4 = await add_node("Phase 4: Launch", parent_id=id1_3, position=4)

    # Personal Development Goals
    id2_1 = await add_node("Skill Acquisition", parent_id=id2, position=1)
    id2_2 = await add_node("Networking", parent_id=id2, position=2)
    id2_3 = await add_node("Health and Wellbeing", parent_id=id2, position=3)

    # Skill Acquisition Sub-points
    id2_1_1 = await add_node("Learn Python", parent_id=id2_1, position=1)
    id2_1_2 = await add_node("Master SQL", parent_id=id2_1, position=2)
    id2_1_3 = await add_node("Public Speaking Course", parent_id=id2_1, position=3)

    # Networking Sub-points
    id2_2_1 = await add_node("Attend Industry Events", parent_id=id2_2, position=1)
    id2_2_2 = await add_node("Connect on LinkedIn", parent_id=id2_2, position=2)
    id2_2_3 = await add_node("Mentorship Program", parent_id=id2_2, position=3)

    # Health and Wellbeing Sub-points
    id2_3_1 = await add_node("Consistent Workout Schedule", parent_id=id2_3, position=1)
    id2_3_2 = await add_node("Mindfulness Practice", parent_id=id2_3, position=2)
    id2_3_3 = await add_node("Nutritional Diet Planning", parent_id=id2_3, position=3)

    # Research Topics for Next Quarter
    id3_1 = await add_node("AI and Machine Learning", parent_id=id3, position=1)
    id3_2 = await add_node("Cybersecurity Trends", parent_id=id3, position=2)
    id3_3 = await add_node("Sustainable Technologies", parent_id=id3, position=3)

    # AI and Machine Learning Sub-points
    id3_1_1 = await add_node("Deep Learning Models", parent_id=id3_1, position=1)
    id3_1_2 = await add_node("Natural Language Processing", parent_id=id3_1, position=2)
    id3_1_3 = await add_node(
        "Computer Vision Applications", parent_id=id3_1, position=3
    )

    # Cybersecurity Trends Sub-points
    id3_2_1 = await add_node("Threat Landscape Analysis", parent_id=id3_2, position=1)
    id3_2_2 = await add_node("Emerging Security Protocols", parent_id=id3_2, position=2)
    id3_2_3 = await add_node("Data Privacy Regulations", parent_id=id3_2, position=3)

    # Sustainable Technologies Sub-points
    id3_3_1 = await add_node(
        "Renewable Energy Innovations", parent_id=id3_3, position=1
    )
    id3_3_2 = await add_node(
        "Resource Management Strategies", parent_id=id3_3, position=2
    )
    id3_3_3 = await add_node("Circular Economy Approaches", parent_id=id3_3, position=3)

    # Additional Random ideas
    id4 = await add_node("Organize Home Office", parent_id=None, position=1)
    id5 = await add_node("Plan a weekend trip", parent_id=None, position=2)
    id6 = await add_node("Read 'Sapiens' ", parent_id=None, position=3)
    id7 = await add_node("Try a new recipe", parent_id=id5, position=1)
    id8 = await add_node("Book a hotel", parent_id=id5, position=2)
