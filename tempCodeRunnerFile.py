def crossedCheckpoint(self, checkpoint_id, time_from_start):
        max_checkpoint = config.SEGMENT_N // 2 - 1

        no_collision = checkpoint_id == -1
        lap_completed = (~no_collision) & (self.prev_checkpoint_id == max_checkpoint) & (checkpoint_id == 0)
        same = (~no_collision) & (~lap_completed) & (checkpoint_id == self.prev_checkpoint_id)
        advanced = (~no_collision) & (~lap_completed) & (checkpoint_id > self.prev_checkpoint_id)
        regressed_raw = (~no_collision) & (~lap_completed) & (checkpoint_id < self.prev_checkpoint_id)
        is_new_wrong = (self.prev_wrong_checkpoint_id == -1) | (checkpoint_id < self.prev_wrong_checkpoint_id)

        regressed = regressed_raw & is_new_wrong
        returning = regressed_raw & (~is_new_wrong)

        self.prev_checkpoint_id = torch.where(lap_completed | advanced, checkpoint_id, self.prev_checkpoint_id)
        self.prev_wrong_checkpoint_id = torch.where(regressed, checkpoint_id, self.prev_wrong_checkpoint_id)

        self.prev_wrong_checkpoint_id = torch.where(
            lap_completed | advanced,
            torch.full_like(self.prev_wrong_checkpoint_id, -1),
            self.prev_wrong_checkpoint_id
        )

        delta = torch.zeros_like(self.points)
        delta = torch.where(advanced, torch.full_like(self.points, 1.0), delta)
        delta = torch.where(lap_completed, 100.0 / time_from_start, delta)
        delta = torch.where(regressed, torch.full_like(self.points, -1.0), delta)

        self.lap_count += lap_completed.to(self.lap_count.dtype)

        self.points += delta
        self.reward += delta

        self.alive &= self.lap_count < config.LAP_AMOUNT