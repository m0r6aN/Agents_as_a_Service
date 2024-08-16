class RoutingAgent(BaseAgent):
    def __init__(self, routing_rules):
        super().__init__(
            known_actions={}, 
            default_prompt="You are a Routing Agent responsible for directing requests to the appropriate agents based on predefined rules. Your role is to ensure that requests are routed efficiently and accurately. Implement fallback mechanisms to handle cases where the primary agent is unavailable or cannot process the request.",
            system_message="You are a Routing Agent tasked with routing requests to different agents according to specific rules. Manage fallback scenarios and ensure that requests are handled effectively. Use predefined routing rules to direct requests to the appropriate agent and implement mechanisms to handle unprocessable or failed requests.",
            max_turns=5
        )
        self.routing_rules = routing_rules  # Define routing rules for agent selection

    def execute(self, request):
        """
        Routes the request to the appropriate agent based on routing rules.
        
        Args:
            request (dict): A dictionary representing the request details.
        
        Returns:
            dict: The response from the selected agent.
        """
        agent = self.select_agent(request)
        if not agent:
            raise ValueError("No suitable agent found for the request")
        return agent.execute(request)

    def select_agent(self, request):
        """
        Selects an agent based on the routing rules and request details.
        
        Args:
            request (dict): A dictionary representing the request details.
        
        Returns:
            BaseAgent: The selected agent for handling the request.
        """
        # Implement logic to select the appropriate agent based on routing rules
        for rule in self.routing_rules:
            if self.matches_rule(rule, request):
                return rule['agent']
        return None

    def matches_rule(self, rule, request):
        """
        Checks if the request matches the given routing rule.
        
        Args:
            rule (dict): The routing rule to check.
            request (dict): A dictionary representing the request details.
        
        Returns:
            bool: True if the request matches the rule, False otherwise.
        """
        # Implement logic to determine if request matches the rule
        pass
