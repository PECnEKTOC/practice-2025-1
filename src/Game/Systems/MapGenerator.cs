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
      public MapGenerator( int width, int height, 
      int maxRooms, int roomMaxSize, int roomMinSize )
      {
         _width = width;
         _height = height;
         _maxRooms = maxRooms;
         _roomMaxSize = roomMaxSize;
         _roomMinSize = roomMinSize;
         _map = new DungeonMap();
      }

      // Generate a new map that is a simple open floor with walls around the outside
      public DungeonMap CreateMap()
      {
         int roomWidth = Game.Random.Next( _roomMinSize, _roomMaxSize );
         int roomHeight = Game.Random.Next( _roomMinSize, _roomMaxSize );
         int roomXPosition = Game.Random.Next( 0, _width - roomWidth - 1 );
         int roomYPosition = Game.Random.Next( 0, _height - roomHeight - 1 );
         
          var newRoom = new Rectangle( roomXPosition, roomYPosition, 
        roomWidth, roomHeight );

        bool newRoomIntersects = _map.Rooms.Any( room => newRoom.Intersects( room ) );

         if ( !newRoomIntersects )
         {
         _map.Rooms.Add( newRoom );
         }

         
         _map.Initialize( _width, _height );
         foreach ( Cell cell in _map.GetAllCells() )
         {
            _map.SetCellProperties( cell.X, cell.Y, true, true, true );
         }

         // Set the first and last rows in the map to not be transparent or walkable
         foreach ( Cell cell in _map.GetCellsInRows( 0, _height - 1 ) )
         {
            _map.SetCellProperties( cell.X, cell.Y, false, false, true );
         }

         // Set the first and last columns in the map to not be transparent or walkable
         foreach ( Cell cell in _map.GetCellsInColumns( 0, _width - 1 ) )
         {
            _map.SetCellProperties( cell.X, cell.Y, false, false, true );
         }

         foreach ( Rectangle room in _map.Rooms )
         {
            CreateRoom( room );
         }
      
         return _map;
      }

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
