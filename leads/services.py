from .models import LeadScoreRule


def calculate_lead_score(lead):
    """
    Calculate the score of a lead based on active scoring rules.
    """

    score = 0

    rules = LeadScoreRule.objects.filter(
        is_active=True
    )

    for rule in rules:

        field_value = getattr(
            lead,
            rule.field,
            ''
        )

        if field_value is None:
            field_value = ''

        field_value = str(field_value).strip().lower()
        rule_value = str(rule.value).strip().lower()

        # Check whether the field has a value
        if rule.operator == 'exists':

            if field_value:
                score += rule.points

        # Check whether field contains a value
        elif rule.operator == 'contains':

            if rule_value in field_value:
                score += rule.points

        # Check exact match
        elif rule.operator == 'equals':

            if field_value == rule_value:
                score += rule.points

        # Check beginning of value
        elif rule.operator == 'starts_with':

            if field_value.startswith(rule_value):
                score += rule.points

    return score