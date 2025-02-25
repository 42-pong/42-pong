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
    tournament_id: 42,
    user_id: 7,
    participation_name: "player_7",
    ranking: 4,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
  {
    id: 2,
    tournament_id: 42,
    user_id: 1,
    participation_name: "player_1",
    ranking: 5,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
  {
    id: 4,
    tournament_id: 4242,
    user_id: 2,
    participation_name: "player_2",
    ranking: 10,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
  {
    id: 3,
    tournament_id: 42,
    user_id: 2,
    participation_name: "player_2",
    ranking: 10,
    created_at: "2025-01-01T00:00:00.000000+09:00",
    updated_at: "2025-01-01T00:30:00.000000+09:00",
  },
];

export {
  sampleUsers,
  sampleMyInfo,
  sampleFriends,
  sampleParticipations,
};
