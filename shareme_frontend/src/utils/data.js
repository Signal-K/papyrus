// Fetch sanity data from this file
export const userQuery = (userId) => {
    const query = `*[_type == "user" && _id == "${userId}"]`;
}