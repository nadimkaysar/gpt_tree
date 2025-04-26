class GameTreeNode:
    def __init__(self, action, reward=0):
        self.action = action
        self.reward = reward
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def print_tree(self, level=0):
        print("  " * level + f"{self.action} (Reward: {self.reward:.2f})")
        for child in self.children:
            child.print_tree(level + 1)

class DBTGameTree:
    def __init__(self, actions):
        self.actions = actions  # Possible DBT actions
        self.root = GameTreeNode("Start")
        self.current_node = self.root  # Start from the root

    def expand_tree(self, reward_data):
        """Expand the tree from the previously selected best action based on reward data."""
        if not self.current_node.children:
            for action, reward in reward_data.items():
                self.current_node.add_child(GameTreeNode(action, reward))
        else:
            new_children = []
            for action, reward in reward_data.items():
                new_children.append(GameTreeNode(action, reward))
            self.current_node.children = new_children

    def select_best_action(self):
        """Select the action with the highest reward and expand from there."""
        if not self.current_node.children:
            return None, 0
        best_action_node = max(self.current_node.children, key=lambda x: x.reward)
        self.current_node = best_action_node  # Move to the best action node
        return best_action_node.action, best_action_node.reward

    def print_tree(self):
        """Print the entire game tree."""
        self.root.print_tree()

def data_extraction(data):
    utility_scores = {}
    utility_score_list = []
    utility_for_mindfullness = 0.0
    for state in data['predictions']["Mindfulness"]["possible_states"]:
        weighted_sum = 0.0
        rewards = state["rewards"]
        
        # Extract necessary Reward & Weight values
        Impact_on_well_being_reward = rewards[0]["Impact_on_well_being_reward"]
        Impact_on_well_being_weight = rewards[0]["Impact_on_well_being_weight"]

        Patient_goal_achievement_reward = rewards[1]["Patient_goal_achievement_reward"]
        Patient_goal_achievement_weight = rewards[1]["Patient_goal_achievement_weight"]

        Patient_satisfaction_reward = rewards[2]["Patient_satisfaction_reward"]
        Patient_satisfaction_weight = rewards[2]["Patient_satisfaction_weight"]

        Feedback_Quality_reward = rewards[3]["Feedback_Quality_reward"]
        Feedback_Quality_weight = rewards[3]["Feedback_Quality_weight"]
        
        # Compute weighted sum based on the provided formula
        weighted_sum = ((Impact_on_well_being_reward * Impact_on_well_being_weight) +
                        (Patient_goal_achievement_reward * Patient_goal_achievement_weight) + 
                        (Patient_satisfaction_reward * Patient_satisfaction_weight) + 
                        (Feedback_Quality_reward * Feedback_Quality_weight))
        
        # Multiply the weighted sum by the probability
        utility_for_mindfullness += state["probability"] * weighted_sum
    utility_score_list.append(float(utility_for_mindfullness))
    utility_scores["Mindfulness"] = float(utility_for_mindfullness)


    utility_for_Distress_Tolerance = 0.0
    for state in data['predictions']["Distress_Tolerance"]["possible_states"]:
        weighted_sum = 0.0
        rewards = state["rewards"]
        
        # Extract necessary Reward & Weight values
        Impact_on_well_being_reward = rewards[0]["Impact_on_well_being_reward"]
        Impact_on_well_being_weight = rewards[0]["Impact_on_well_being_weight"]

        Patient_goal_achievement_reward = rewards[1]["Patient_goal_achievement_reward"]
        Patient_goal_achievement_weight = rewards[1]["Patient_goal_achievement_weight"]

        Patient_satisfaction_reward = rewards[2]["Patient_satisfaction_reward"]
        Patient_satisfaction_weight = rewards[2]["Patient_satisfaction_weight"]

        Feedback_Quality_reward = rewards[3]["Feedback_Quality_reward"]
        Feedback_Quality_weight = rewards[3]["Feedback_Quality_weight"]
        
        # Compute weighted sum based on the provided formula
        weighted_sum = ((Impact_on_well_being_reward * Impact_on_well_being_weight) + 
                        (Patient_goal_achievement_reward * Patient_goal_achievement_weight) + 
                        (Patient_satisfaction_reward * Patient_satisfaction_weight) + 
                        (Feedback_Quality_reward * Feedback_Quality_weight))
        
        # Multiply the weighted sum by the probability
        utility_for_Distress_Tolerance += state["probability"] * weighted_sum
    utility_score_list.append(float(utility_for_Distress_Tolerance))
    utility_scores["Distress Tolerance"] = float(utility_for_Distress_Tolerance)


    utility_for_Interpersonal_Effectiveness = 0.0
    for state in data['predictions']["Interpersonal_Effectiveness"]["possible_states"]:
        weighted_sum = 0.0
        rewards = state["rewards"]
        
        # Extract necessary Reward & Weight values
        Impact_on_well_being_reward = rewards[0]["Impact_on_well_being_reward"]
        Impact_on_well_being_weight = rewards[0]["Impact_on_well_being_weight"]

        Patient_goal_achievement_reward = rewards[1]["Patient_goal_achievement_reward"]
        Patient_goal_achievement_weight = rewards[1]["Patient_goal_achievement_weight"]

        Patient_satisfaction_reward = rewards[2]["Patient_satisfaction_reward"]
        Patient_satisfaction_weight = rewards[2]["Patient_satisfaction_weight"]

        Feedback_Quality_reward = rewards[3]["Feedback_Quality_reward"]
        Feedback_Quality_weight = rewards[3]["Feedback_Quality_weight"]
        
        # Compute weighted sum based on the provided formula
        weighted_sum = ((Impact_on_well_being_reward * Impact_on_well_being_weight) + 
                        (Patient_goal_achievement_reward * Patient_goal_achievement_weight) + 
                        (Patient_satisfaction_reward * Patient_satisfaction_weight) + 
                        (Feedback_Quality_reward * Feedback_Quality_weight))
        
        # Multiply the weighted sum by the probability
        utility_for_Interpersonal_Effectiveness += state["probability"] * weighted_sum
    utility_score_list.append(float(utility_for_Interpersonal_Effectiveness))
    utility_scores["Interpersonal Effectiveness"] = float(utility_for_Interpersonal_Effectiveness)

    utility_for_Emotion_Regulation = 0.0
    for state in data['predictions']["Emotion_Regulation"]["possible_states"]:
        weighted_sum = 0.0
        rewards = state["rewards"]
        
        # Extract necessary Reward & Weight values
        Impact_on_well_being_reward = rewards[0]["Impact_on_well_being_reward"]
        Impact_on_well_being_weight = rewards[0]["Impact_on_well_being_weight"]

        Patient_goal_achievement_reward = rewards[1]["Patient_goal_achievement_reward"]
        Patient_goal_achievement_weight = rewards[1]["Patient_goal_achievement_weight"]

        Patient_satisfaction_reward = rewards[2]["Patient_satisfaction_reward"]
        Patient_satisfaction_weight = rewards[2]["Patient_satisfaction_weight"]

        Feedback_Quality_reward = rewards[3]["Feedback_Quality_reward"]
        Feedback_Quality_weight = rewards[3]["Feedback_Quality_weight"]
        
        # Compute weighted sum based on the provided formula
        weighted_sum = ((Impact_on_well_being_reward * Impact_on_well_being_weight) + 
                        (Patient_goal_achievement_reward * Patient_goal_achievement_weight) + 
                        (Patient_satisfaction_reward * Patient_satisfaction_weight) + 
                        (Feedback_Quality_reward * Feedback_Quality_weight))
        
        # Multiply the weighted sum by the probability
        utility_for_Emotion_Regulation += state["probability"] * weighted_sum
    utility_score_list.append(float(utility_for_Emotion_Regulation))
    utility_scores["Emotion Regulation"] = float(utility_for_Emotion_Regulation)
    print("All Utility Scores:", utility_scores)
    return utility_scores


actions = ["Mindfulness", "Distress Tolerance", "Interpersonal Effectiveness", "Emotion Regulation"]
game_tree = DBTGameTree(actions)

def dataImport(reward_data):
    extracted_rewards = data_extraction(reward_data)
    game_tree.expand_tree(extracted_rewards)

    best_action, reward = game_tree.select_best_action()
    print(f"Best Action = {best_action}, Reward = {reward:.2f}")
    game_tree.expand_tree(extracted_rewards)

    # Print the final game tree
    game_tree.print_tree()
    return best_action


