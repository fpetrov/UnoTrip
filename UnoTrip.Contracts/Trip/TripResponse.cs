﻿using UnoTrip.Domain.Entities;

namespace UnoTrip.Contracts.Trip;

public record TripResponse(
    Guid Uuid,
    string Name,
    string Description,
    List<Note> Notes,
    List<long> SubscribersIds,
    List<Location> Locations);