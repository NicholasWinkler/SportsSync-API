# SportsSyncApi/views/favorite_teams.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from ..models.favorite_team import FavoriteTeam
import logging

logger = logging.getLogger(__name__)

class FavoriteTeamView(APIView):
    """
    API View for handling favorite team operations.
    Requires token authentication.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get all favorite teams for the current user.
        """
        try:
            # Log the request
            logger.info(f"Getting favorites for user: {request.user.username}")
            
            # Get all favorite teams for the current user
            favorites = FavoriteTeam.objects.filter(user=request.user)
            favorite_teams = [favorite.team_id for favorite in favorites]
            
            logger.info(f"Successfully retrieved favorites for {request.user.username}: {favorite_teams}")
            
            return Response({
                'favorite_teams': favorite_teams,
                'message': 'Favorite teams retrieved successfully'
            })
            
        except Exception as e:
            logger.error(f"Error getting favorites: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Failed to retrieve favorite teams'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
        Add a team to user's favorites.
        Requires team_id in request body.
        """
        try:
            team_id = request.data.get('team_id')
            
            if not team_id:
                return Response(
                    {'error': 'team_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            logger.info(f"Adding team {team_id} to favorites for user: {request.user.username}")

            # Try to create new favorite, or get existing one
            favorite, created = FavoriteTeam.objects.get_or_create(
                user=request.user,
                team_id=team_id
            )

            if created:
                logger.info(f"Team {team_id} added to favorites for {request.user.username}")
                return Response(
                    {'message': 'Team added to favorites'},
                    status=status.HTTP_201_CREATED
                )
            else:
                logger.info(f"Team {team_id} already in favorites for {request.user.username}")
                return Response(
                    {'message': 'Team already in favorites'},
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            logger.error(f"Error adding favorite: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Failed to add team to favorites'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, team_id):
        """
        Remove a team from user's favorites.
        Requires team_id in URL.
        """
        try:
            logger.info(f"Attempting to delete team {team_id} from favorites for user: {request.user.username}")
            
            # Find the favorite team entry
            favorite = get_object_or_404(
                FavoriteTeam,
                user=request.user,
                team_id=team_id
            )
            
            # Delete it
            favorite.delete()
            
            logger.info(f"Successfully removed team {team_id} from favorites for {request.user.username}")
            
            return Response(
                {'message': 'Team removed from favorites'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except FavoriteTeam.DoesNotExist:
            logger.warning(f"Team {team_id} not found in favorites for {request.user.username}")
            return Response(
                {'error': 'Team not found in favorites'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error removing favorite: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Failed to remove team from favorites'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, team_id=None):
        """
        Not supported - returns 405 Method Not Allowed
        """
        return Response(
            {'error': 'PUT method not supported for favorite teams'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def patch(self, request, team_id=None):
        """
        Not supported - returns 405 Method Not Allowed
        """
        return Response(
            {'error': 'PATCH method not supported for favorite teams'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )