const SAMPLE_COUNT = 30; // userId: 1 ~ SAMPLE_COUNT

const MY_USER_ID = 1;
const MY_EMAIL = "mock@example.com";

const createSampleUser = (number) =>
  Object.freeze({
    id: number,
    username: `pong${number}`,
    display_name: `DISPLAY${number}`,
    avatar: "/media/avatars/sample.png",
  });

const sampleUsers = Array.from({ length: SAMPLE_COUNT }).map(
  (_, idx) => createSampleUser(idx + 1),
);

const sampleMyInfo = {
  ...sampleUsers.find(({ id }) => id === MY_USER_ID),
  email: MY_EMAIL,
};

const createSampleFriend = (idx) =>
  Object.freeze({
    user_id: MY_USER_ID,
    friend_user_id: sampleUsers[idx].id,
    friend: {
      username: sampleUsers[idx].username,
      display_name: sampleUsers[idx].display_name,
      avatar: sampleUsers[idx].avatar,
    },
  });

const sampleFriends = Array.from({ length: SAMPLE_COUNT / 2 })
  .map((_, idx) => createSampleFriend(2 * idx))
  .filter((friend) => friend.user_id !== friend.friend_user_id);

const sampleParticipations = [
  {
    id: 1,
    tournament_id: 41,
    user_id: 1,
    participation_name: "john_doe",
    ranking: 4,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
  {
    id: 1,
    tournament_id: 42,
    user_id: 1,
    participation_name: "john",
    ranking: 4,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
  {
    id: 2,
    tournament_id: 42,
    user_id: 2,
    participation_name: "alice",
    ranking: 5,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
  {
    id: 4,
    tournament_id: 42,
    user_id: 3,
    participation_name: "bob",
    ranking: 10,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
  {
    id: 3,
    tournament_id: 42,
    user_id: 4,
    participation_name: "charlie",
    ranking: 10,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
  {
    id: 1,
    tournament_id: 43,
    user_id: 1,
    participation_name: "john",
    ranking: 4,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
  {
    id: 2,
    tournament_id: 43,
    user_id: 2,
    participation_name: "alice",
    ranking: 5,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
  {
    id: 4,
    tournament_id: 43,
    user_id: 3,
    participation_name: "bob",
    ranking: 10,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
  {
    id: 3,
    tournament_id: 43,
    user_id: 4,
    participation_name: "charlie",
    ranking: 10,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
];

const sampleTournaments = [
  {
    id: 41,
    status: "waiting",
    created_at: "2025-02-23T00:05:56.611173+09:00",
    updated_at: "2025-02-23T00:05:56.611186+09:00",
    rounds: [],
  },
  {
    id: 42,
    status: "on_going",
    created_at: "2025-02-23T00:06:24.433761+09:00",
    updated_at: "2025-02-23T00:06:24.433775+09:00",
    rounds: [
      {
        round_number: 1,
        status: "completed",
        created_at: "2025-02-23T00:06:43.507125+09:00",
        updated_at: "2025-02-23T00:06:43.507140+09:00",
        matches: [
          {
            id: 1,
            round_id: 1,
            status: "not_started",
            created_at: "2025-02-23T00:43:46.619483+09:00",
            updated_at: "2025-02-23T00:43:46.619495+09:00",
            participations: [],
          },
          {
            id: 2,
            round_id: 1,
            status: "completed",
            created_at: "2025-02-23T00:44:00.342844+09:00",
            updated_at: "2025-02-23T00:44:00.342858+09:00",
            participations: [
              {
                user_id: 3,
                team: "1",
                is_win: true,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                ],
              },
              {
                user_id: 4,
                team: "2",
                is_win: false,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:18.735550+09:00",
                    pos_x: 0,
                    pos_y: 100,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 0,
                    pos_y: 380,
                  },
                ],
              },
            ],
          },
          {
            id: 4,
            round_id: 1,
            status: "canceled",
            created_at: "2025-02-23T00:44:04.645508+09:00",
            updated_at: "2025-02-23T00:44:04.645521+09:00",
            participations: [
              {
                user_id: 2,
                team: "1",
                is_win: true,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                ],
              },
              {
                user_id: 1,
                team: "2",
                is_win: false,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:18.735550+09:00",
                    pos_x: 0,
                    pos_y: 100,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 0,
                    pos_y: 380,
                  },
                ],
              },
            ],
          },
        ],
      },
      {
        round_number: 2,
        status: "on_going",
        created_at: "2025-02-23T00:06:43.507125+09:00",
        updated_at: "2025-02-23T00:06:43.507140+09:00",
        matches: [
          {
            id: 6,
            round_id: 8,
            status: "on_going",
            created_at: "2025-02-23T00:43:46.619483+09:00",
            updated_at: "2025-02-23T00:43:46.619495+09:00",
            participations: [
              {
                user_id: 2,
                team: "1",
                is_win: false,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                ],
              },
              {
                user_id: 3,
                team: "2",
                is_win: false,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:18.735550+09:00",
                    pos_x: 0,
                    pos_y: 100,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 0,
                    pos_y: 380,
                  },
                ],
              },
            ],
          },
        ],
      },
    ],
  },
  {
    id: 43,
    status: "completed",
    created_at: "2025-02-23T00:06:24.433761+09:00",
    updated_at: "2025-02-23T00:06:24.433775+09:00",
    rounds: [
      {
        round_number: 1,
        status: "on_going",
        created_at: "2025-02-23T00:06:43.507125+09:00",
        updated_at: "2025-02-23T00:06:43.507140+09:00",
        matches: [
          {
            id: 1,
            round_id: 1,
            status: "not_started",
            created_at: "2025-02-23T00:43:46.619483+09:00",
            updated_at: "2025-02-23T00:43:46.619495+09:00",
            participations: [],
          },
          {
            id: 2,
            round_id: 1,
            status: "completed",
            created_at: "2025-02-23T00:44:00.342844+09:00",
            updated_at: "2025-02-23T00:44:00.342858+09:00",
            participations: [
              {
                user_id: 3,
                team: "1",
                is_win: true,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                ],
              },
              {
                user_id: 4,
                team: "2",
                is_win: false,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:18.735550+09:00",
                    pos_x: 0,
                    pos_y: 100,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 0,
                    pos_y: 380,
                  },
                ],
              },
            ],
          },
          {
            id: 4,
            round_id: 1,
            status: "canceled",
            created_at: "2025-02-23T00:44:04.645508+09:00",
            updated_at: "2025-02-23T00:44:04.645521+09:00",
            participations: [
              {
                user_id: 2,
                team: "1",
                is_win: true,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                ],
              },
              {
                user_id: 1,
                team: "2",
                is_win: false,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:18.735550+09:00",
                    pos_x: 0,
                    pos_y: 100,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 0,
                    pos_y: 380,
                  },
                ],
              },
            ],
          },
        ],
      },
      {
        round_number: 2,
        status: "completed",
        created_at: "2025-02-23T00:06:43.507125+09:00",
        updated_at: "2025-02-23T00:06:43.507140+09:00",
        matches: [
          {
            id: 6,
            round_id: 8,
            status: "completed",
            created_at: "2025-02-23T00:43:46.619483+09:00",
            updated_at: "2025-02-23T00:43:46.619495+09:00",
            participations: [
              {
                user_id: 2,
                team: "1",
                is_win: true,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 600,
                    pos_y: 10,
                  },
                ],
              },
              {
                user_id: 3,
                team: "2",
                is_win: false,
                scores: [
                  {
                    created_at: "2025-02-11T14:01:18.735550+09:00",
                    pos_x: 0,
                    pos_y: 100,
                  },
                  {
                    created_at: "2025-02-11T14:01:32.315450+09:00",
                    pos_x: 0,
                    pos_y: 380,
                  },
                ],
              },
            ],
          },
        ],
      },
    ],
  },
];

export {
  sampleUsers,
  sampleMyInfo,
  sampleFriends,
  sampleParticipations,
  sampleTournaments,
};
