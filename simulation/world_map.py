import numpy as np
from simulation.direction import Direction


class WorldMap(object):
    def __init__(self, grid=np.empty((0, 0), dtype=object)):
        self.grid = grid

    def can_move_to(self, target_location):
        return True

    def get_world_view_centred_at(self, view_location, distance_to_edge):
        '''
                            world_map
        +-----------------------------------------------+
        |                                               |
        |                                               |
        |                                               |
        |                + map_corner                   |
        |                |                              |
        |                v                              |
        |                     view_map                  |
        |                +----------------+             |
        |                |                |             |
        |                |                |             |
        |                |                |             |
        |                |                |             |
        |                |                |             |
        |                |                |             |
        |                +----------------+             |
        |                                               |
        |                                               |
        |                                               |
        |                                               |
        +-----------------------------------------------+

        '''
        num_grid_rows, num_grid_cols = self.grid.shape
        num_view_rows, num_view_cols = 2 * distance_to_edge + 1, 2 * distance_to_edge + 1

        view_map_corner = view_location - Direction(distance_to_edge, distance_to_edge)

        # Non-cropped indices
        row_start = view_map_corner.row
        row_exclusive_end = row_start + num_view_rows

        col_start = view_map_corner.col
        col_exclusive_end = col_start + num_view_cols

        # Cropped indices
        cropped_row_start = max(0, row_start)
        cropped_row_exclusive_end = min(num_grid_rows, row_start + num_view_rows)

        cropped_col_start = max(0, col_start)
        cropped_col_exclusive_end = min(num_grid_cols, col_start + num_view_cols)

        assert 0 <= cropped_row_start < cropped_row_exclusive_end <= num_grid_rows
        assert 0 <= cropped_col_start < cropped_col_exclusive_end <= num_grid_cols

        # Extract cropped region
        cropped_view_map = self.grid[cropped_row_start:cropped_row_exclusive_end, cropped_col_start:cropped_col_exclusive_end]

        # Pad map
        num_pad_rows_before = cropped_row_start - row_start
        num_pad_rows_after = row_exclusive_end - cropped_row_exclusive_end

        num_pad_cols_before = cropped_col_start - col_start
        num_pad_cols_after = col_exclusive_end - cropped_col_exclusive_end

        padded_view_map = np.pad(cropped_view_map,
                                 ((num_pad_rows_before, num_pad_rows_after), (num_pad_cols_before, num_pad_cols_after)),
                                 mode='constant', constant_values=-1
                                 )

        return WorldMap(padded_view_map)
