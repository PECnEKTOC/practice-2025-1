using System.Linq;
using RogueSharp;
using RogueSharpV3Tutorial.Core;

namespace RogueSharpV3Tutorial.Systems
{
   public class MapGenerator
   {
      private readonly int _width;
      private readonly int _height;
      private readonly int _maxRooms;
      private readonly int _roomMaxSize;
      private readonly int _roomMinSize;

      private readonly DungeonMap _map;

      // Constructing a new MapGenerator requires the dimensions of the maps it will create
      // as well as the sizes and maximum number of rooms
      public MapGenerator( int width, int height, int maxRooms, int roomMaxSize, int roomMinSize )
      {
         _width = width;
         _height = height;
         _maxRooms = maxRooms;
         _roomMaxSize = roomMaxSize;
         _roomMinSize = roomMinSize;
         _map = new DungeonMap();
      }

      // Generate a new map that places rooms randomly
      public DungeonMap CreateMap()
      {
         // Set the properties of all cells to false
         _map.Initialize( _width, _height );

         // Try to place as many rooms as the specified maxRooms
         for ( int r = 0; r < _maxRooms; r++ )
         {
            // Determine a the size and position of the room randomly
            int roomWidth = Game.Random.Next( _roomMinSize, _roomMaxSize );
            int roomHeight = Game.Random.Next( _roomMinSize, _roomMaxSize );
            int roomXPosition = Game.Random.Next( 0, _width - roomWidth - 1 );
            int roomYPosition = Game.Random.Next( 0, _height - roomHeight - 1 );

            // All of our rooms can be represented as Rectangles
            var newRoom = new Rectangle( roomXPosition, roomYPosition, roomWidth, roomHeight );

            // Check to see if the room rectangle intersects with any other rooms
            bool newRoomIntersects = _map.Rooms.Any( room => newRoom.Intersects( room ) );
            // As long as it doesn't intersect add it to the list of rooms. Otherwise throw it out
            if ( !newRoomIntersects )
            {
               _map.Rooms.Add( newRoom );
            }
         }
         // Iterate through each room that we wanted placed and call CreateRoom to make it
         foreach ( Rectangle room in _map.Rooms )
         {
            CreateRoom( room );
         }

         return _map;
      }

      // Given a rectangular area on the map
      // set the cell properties for that area to true
      private void CreateRoom( Rectangle room )
      {
         for ( int x = room.Left + 1; x < room.Right; x++ )
         {
            for ( int y = room.Top + 1; y < room.Bottom; y++ )
            {
               _map.SetCellProperties( x, y, true, true, true );
            }
         }
      }
   }
}
