from django.contrib.auth.tokens import PasswordResetTokenGenerator  # Import Django's built-in token generator
import six  # Library for consistent text encoding across Python 2 and 3

# Custom token generator for account activation
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for user account activation.
    This generator extends Django's PasswordResetTokenGenerator to create a unique token
    that is used for email-based account activation.
    """

    def _make_hash_value(self, user, timestamp):
        """
        Generates a secure hash value for the user.
        This hash value is used to create a token for email verification.

        Args:
        - user: The user object for whom the token is being created.
        - timestamp: A timestamp that ensures the token's uniqueness for a particular time frame.

        The hash value includes:
        - The user's primary key (user.pk)
        - The timestamp for when the token was created
        - The user's "is_active" status, ensuring that a new token is required if the user's status changes

        Returns:
        - A combined string that serves as the hash value for the token.
        """
        return (
            six.text_type(user.pk) + 
            six.text_type(timestamp) + 
            six.text_type(user.is_active)
        )

# Create an instance of the custom account activation token generator
account_activation_token = AccountActivationTokenGenerator()
