import re
from datetime import datetime, timedelta
from django.db.utils import IntegrityError
from django.utils.timezone import now
from users.models import UserIP, SearchLog


def is_valid_email(email):
    """
    Check if email is valid or not
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_regex, email):
        return True
    else:
        return False


class TrackUserIP:
    @staticmethod
    def track_ip(request, query):
        """
        Tracks the IP address of a request.
        """
        ip = TrackUserIP.get_client_ip(request)

        if ip:
            try:
                current_time = now()
                five_minutes_ago = current_time - timedelta(minutes=5)
                user_ip, created = UserIP.objects.get_or_create(ip_address=ip)
                if user_ip.is_blocked:
                    return True

                # Check if the user makes a request within 30 seconds after 5 minutes
                if user_ip.last_request_time:
                    if (current_time - user_ip.last_request_time).total_seconds() <= 5 and user_ip.request_count >= 15:
                        user_ip.is_blocked = True
                        user_ip.save()
                        return True

                # If the last request was more than 5 minutes ago, reset the count
                if not user_ip.last_request_time:
                    user_ip.request_count = 1
                elif user_ip.last_request_time < five_minutes_ago:
                    user_ip.request_count = 1  # Reset count after 5 minutes
                else:
                    user_ip.request_count += 1  # Increment count

                # Update the last request time
                user_ip.last_request_time = current_time
                user_ip.save()

                # Creates the search log for the keyword
                SearchLog.objects.create(user_ip=user_ip, keyword=query)
                return False

            except IntegrityError:
                pass

    @staticmethod
    def get_client_ip(request):
        """
        Get the client's IP address from the request headers.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # Get the first IP in the list
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
