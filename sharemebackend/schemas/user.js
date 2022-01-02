export default {
    name: 'user',
    title: 'User',
    type: 'document',
    fields: [
        { // User field for the user
            name: 'userName',
            title: 'UserName',
            type: 'string'
        },
        { // Image field for the user
            name: 'image',
            title: 'Image',
            type: 'string' // URL for link to image
        },
    ]
}