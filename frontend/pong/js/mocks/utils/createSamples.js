const MY_USER_ID = 21;
const SAMPLE_COUNT = 30;

const createSampleUser = (number) =>
  Object.freeze({
    id: `${number}`,
    username: `pong${number}`,
    display_name: `DISPLAY${number}`,
    avatar: "https://placehold.co/30",
  });

const sampleUsers = Array.from({ length: SAMPLE_COUNT }).map(
  (_, idx) => createSampleUser(idx + 1),
);

const createSampleFriend = (idx) =>
  Object.freeze({
    user_id: `${MY_USER_ID}`,
    friend_user_id: sampleUsers[idx].id,
    friend: {
      username: sampleUsers[idx].username,
      display_name: sampleUsers[idx].display_name,
      avatar: sampleUsers[idx].avatar,
    },
  });

const sampleFriends = Array.from({ length: SAMPLE_COUNT / 2 }).map(
  (_, idx) => createSampleFriend(2 * idx),
);

export { sampleUsers, sampleFriends };
