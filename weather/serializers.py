from rest_framework import serializers


class CoordinatesSerializer(serializers.Serializer):
    """Serializer for Coordinates to check that are valid."""
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def validate_latitude(self, latitude):
        """Checks the latitude is between valid values"""
        if not(-90 <= latitude <= 90):
            raise serializers.ValidationError("Latitude must be a value between -90 and 90.")
        return latitude

    def validate_longitude(self, longitude):
        """Checks the longitude is between valid values."""
        if not(-180 <= longitude <= 180):
            raise serializers.ValidationError("Longitude must be a value between -180 and 180.")
        return longitude
