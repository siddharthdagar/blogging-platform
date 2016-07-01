# blogging-platform API documentation

#### Contents

- [Overview](#1-overview)
- [Resources](#2-resources)
  - [Posts](#21-posts)
  - [Comments](#22-comments)
- [Testing](#3-testing)

## 1. Overview
All APIs are RESTful and JSON based.

## 2. Resources

### 2.1 Posts

#### Creating a post
Creates a blog post

```
POST http://<domain>/posts/
```
Example request:
```
POST /posts HTTP/1.1
Host: <domain>
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8
{
    "title": "post 10",
    "text": "something\n\npara 2\n\npara 3\n\npara 4"
}
```

Description of fields:

| Parameter  | Type    | Required? | Description                               |
| ---------- | ------- | --------- | -------------------------------           |
| title     | string  | required  | The title of the post. Max length is 200  |
| text      | string  | required  | The body text of the post.                |

Example response:
```
HTTP/1.1 200 OK
Content-Type: application/json
{
  "message": "",
  "result": {
    "post_uid": "389f8cc3dbe344eb9e3e7e8406b720ee"
  },
  "error": 0
}
```
Description of response:

| Field      | Type     | Description    |
| --------- | ------- | -------------- |
| post_uid   | string  | Unique (random) identifier for the post |

Possible Errors:

| Error code    | Description      |
| ------------ | ----------------------------------------- |
| 400 Bad Request | Required fields were invalid   |


#### Getting list of posts (list-mode)

```
GET http://<domain>/posts/?page=1&size=5
```
Description of GET parameters:

| Parameter  | Type     | Required?   | Description       |
| --------- | -------- | ----------- | ----------------- |
| page       | number   | optional    | Required for getting paginated results based on the size provided. If this is not provided, then all the posts are fetched     |
| size       | number   | optional    | If not provided, defualt is taken as 5   |

Example response:
```
HTTP/1.1 200 OK
Content-Type: application/json
{
  "message": "",
  "result": {
    "pagination_info": {
      "per_page": 5,
      "num_pages": 3
    },
    "data": [
      {
        "text": "para1 1\n\npara 2\n\nmore\n\npara 3\n2nd line",
        "uid": "318cb75bc6974794b389aab52a6479d1",
        "title": "hello"
      },
      {
        "text": "siddharth\n\nblackbuck\n\nsomething else",
        "uid": "b4daae3d563a40d6ba09542cd5cad524",
        "title": "post 2"
      },
      {
        "text": "siddharth\n\nblackbuck\n\nsomething else",
        "uid": "fb94462fdc1647d8829facd8fcb3a898",
        "title": "post 3"
      },
      {
        "text": "siddharth\n\nblackbuck\n\nsomething else",
        "uid": "16ac30327dba4913881ea78d484b521a",
        "title": "post 4"
      },
      {
        "text": "siddharth\n\nblackbuck\n\nsomething else",
        "uid": "d30e7e154bbe4526beb2cb4f2fff5e91",
        "title": "post 5"
      }
    ]
  },
  "error": 0
}
```

#### Getting details for a particular post (full-mode)

```
GET http://<domain>/posts/{{postUid}}?fetch_comments=1
```
Where postUid is the unique identifier for the post

Description of parameters:

| Parameter  | Type    | Required? | Description                    |
| --------- | ------- | --------- | ------------------------------ |
| fetch_comments | number       | optional   | If a non-zero value is provided, then comments for each section (paragraph) of the post are also fetched nested within the sections (see sample response) |

Example response:
```
HTTP/1.1 200 OK
Content-Type: application/json
{
  "message": "",
  "result": {
    "data": {
      "dt_added": 1467277275000,
      "uid": "318cb75bc6974794b389aab52a6479d1",
      "components": [
        {
          "order_rank": 1,
          "text": "para1 1",
          "comments": [
            {
              "text": "comment 3",
              "component_id": 1,
              "id": 3
            }
          ],
          "post_id": 1,
          "comp_type": 1,
          "id": 1,
          "dt_added": 1467277275000
        },
        {
          "order_rank": 2,
          "text": "para 2",
          "post_id": 1,
          "comp_type": 1,
          "id": 2,
          "dt_added": 1467277275000
        },
        {
          "order_rank": 2,
          "text": "more",
          "post_id": 1,
          "comp_type": 1,
          "id": 7,
          "dt_added": null
        },
        {
          "order_rank": 3,
          "text": "para 3\n2nd line",
          "comments": [
            {
              "text": "comment 1",
              "component_id": 3,
              "id": 1
            },
            {
              "text": "comment 2",
              "component_id": 3,
              "id": 2
            }
          ],
          "post_id": 1,
          "comp_type": 1,
          "id": 3,
          "dt_added": 1467277275000
        }
      ],
      "title": "hello"
    }
  },
  "error": 0
}
```
Descripton of response:

| Field      | Type     | Description    |
| --------- | ------- | -------------- |
| data.dt_added | number  | Epoch in ms. The time when the post was added |
| data.uid   | string | The post uid |
| data.components | list | The various components (paragraphs) of the post |
| data.components[0].order_rank | number | The relative position of the component within the post |
| data.components[0].text | string | Text of the component |
| data.components[0].post_id | number | The id of the post (can be ignored) |
| data.components[0].comp_type | number | Enum describing the component type. Right now only - 1 (Paragraph) |
| data.components[0].id | number | The unique identifier of the component |
| data.components[0].dt_added | number | Epoch in ms. The time when the paragraph was added |
| data.components[0].comments | list | Comments for the component |
|  .text  | string | comment text |
|  .id    | number | unique id of the comment |
|  .component_id | number | unique id of the component to which the comment is attached |


Possible Errors:

| Error code    | Description      |
| ------------ | ----------------------------------------- |
| 404 Not found | No details were found for the given postUid |


### 2.2 Comments

#### Create a comment

```
POST http://<domain>/posts/{{postUid}}/comments/
```
Where postUid is the unique identifier of the post to which the commented upon component belongs.

Example request:
```
POST /posts HTTP/1.1
Host: <domain>
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8
{
    "component_id": 1,
    "text": "comment 3"
}
```

Description of fields:

| Parameter  | Type    | Required? | Description                    |
| --------- | ------- | --------- | ------------------------------ |
| component_id | number | required   | The unique identifier for the component (paragraph) which is being commented on |
| text            | string       | required   | The text of the comment.                |

Example response:
```
HTTP/1.1 200 OK
Content-Type: application/json
{
  "message": "",
  "result": {
    "comment_id": 3
  },
  "error": 0
}
```

Description of response:

| Field      | Type     | Description    |
| --------- | ------- | -------------- |
| comment_id   | number  | Unique identifier for the comment |

Possible Errors:

| Error code    | Description      |
| ------------ | ----------------------------------------- |
| 400 Bad Request | Required fields were invalid OR no component with given component_id could be found for the given post  |
| 404 Not found | No post was found for the given postUid|


#### Get comments for a post

```
GET http://<domain>/posts/{{postUid}}/comments/
```

Example response:
```
HTTP/1.1 200 OK
Content-Type: application/json
{
  "message": "",
  "result": {
    "data": [
      {
        "text": "comment 1",
        "component_id": 3,
        "id": 1
      },
      {
        "text": "comment 2",
        "component_id": 3,
        "id": 2
      },
      {
        "text": "comment 3",
        "component_id": 1,
        "id": 3
      }
    ]
  },
  "error": 0
}
```
Description of response:

| Field      | Type     | Description    |
| --------- | ------- | -------------- |
| data      | list  | List of comments for the post |
| data[0].text | string | Comment text |
| data[0].component_id | number | Unique identifier of the component to which the comment was attached |
| data[0].id  | number | Unique identifier of the comment |

Possible Errors:

| Error code    | Description      |
| ------------ | ----------------------------------------- |
| 404 Not found | No post was found for given postUid  |


## 3. Testing

Testing can be done via api testing client (such as POSTman). Here examples have been demonstrated using cURL.
Assuming that the app is hosted on localhost:8001

### 3.1 Posts

#### Creating a post

```
curl -i --data '{"title": "post 1", "text": "para1\n\npara2\n\npara3"}' localhost:8001/posts/

HTTP/1.0 200 OK
Date: Fri, 01 Jul 2016 10:06:28 GMT
Server: WSGIServer/0.1 Python/2.7.6
X-Frame-Options: SAMEORIGIN
Content-Type: application/json

{"message": "", "result": {"post_uid": "08ced364c4584a1785fcc4d7ee9d14f7"}, "error": 0}
```

Create 3 more posts
```
curl -i --data '{"title": "post 2", "text": "para1\n\npara2\n\npara3"}' localhost:8001/posts/
curl -i --data '{"title": "post 3", "text": "para1\n\npara2\n\npara3"}' localhost:8001/posts/
curl -i --data '{"title": "post 4", "text": "para1\n\npara2\n\npara3"}' localhost:8001/posts/
```

#### Fetching the posts (list-mode)
```
curl -i --get --data "page=1&size=2" localhost:8001/posts/

HTTP/1.0 200 OK
Date: Fri, 01 Jul 2016 10:07:57 GMT
Server: WSGIServer/0.1 Python/2.7.6
X-Frame-Options: SAMEORIGIN
Content-Type: application/json

{"message": "", "result": {"pagination_info": {"per_page": 2, "num_pages": 2}, "data": [{"text": "para1\n\npara2\n\npara3", "uid": "08ced364c4584a1785fcc4d7ee9d14f7", "title": "post 1"}, {"text": "para1\n\npara2\n\npara3", "uid": "9095b0214c53431c9e3218d60001d81c", "title": "post 2"}]}, "error": 0}
```

#### Fetching details of a particular post (full-mode)
```
curl -i localhost:8001/posts/08ced364c4584a1785fcc4d7ee9d14f7/
HTTP/1.0 200 OK
Date: Fri, 01 Jul 2016 10:10:01 GMT
Server: WSGIServer/0.1 Python/2.7.6
X-Frame-Options: SAMEORIGIN
Content-Type: application/json

{"message": "", "result": {"data": {"dt_added": 1467367588000, "uid": "08ced364c4584a1785fcc4d7ee9d14f7", "components": [{"order_rank": 1, "text": "para1", "post_id": 1, "comp_type": 1, "id": 1, "dt_added": 1467367588000}, {"order_rank": 2, "text": "para2", "post_id": 1, "comp_type": 1, "id": 2, "dt_added": 1467367588000}, {"order_rank": 3, "text": "para3", "post_id": 1, "comp_type": 1, "id": 3, "dt_added": 1467367588000}], "title": "post 1"}}, "error": 0}
```

Comments can be fetched by passing the fetch_comments parameter as GET parameter

```
curl -i --get --data "fetch_comments=1" localhost:8001/posts/08ced364c4584a1785fcc4d7ee9d14f7/
```
No comments will be fetched since none have been added.

### 3.2 Comments

#### Adding comments to a component (paragraph) of a post
```
curl -i --data '{"component_id": 1, "text": "comment 1"}' localhost:8001/posts/08ced364c4584a1785fcc4d7ee9d14f7/comments/

HTTP/1.0 200 OK
Date: Fri, 01 Jul 2016 10:13:06 GMT
Server: WSGIServer/0.1 Python/2.7.6
X-Frame-Options: SAMEORIGIN
Content-Type: application/json

{"message": "", "result": {"comment_id": 1}, "error": 0}
```
Adding more comments
```
curl -i --data '{"component_id": 1, "text": "comment 2"}' localhost:8001/posts/08ced364c4584a1785fcc4d7ee9d14f7/comments/
curl -i --data '{"component_id": 2, "text": "comment 3"}' localhost:8001/posts/08ced364c4584a1785fcc4d7ee9d14f7/comments/
```

Again trying to fetch comments in full-mode
```
curl -i --get --data "fetch_comments=1" localhost:8001/posts/08ced364c4584a1785fcc4d7ee9d14f7/

HTTP/1.0 200 OK
Date: Fri, 01 Jul 2016 10:14:40 GMT
Server: WSGIServer/0.1 Python/2.7.6
X-Frame-Options: SAMEORIGIN
Content-Type: application/json

{"message": "", "result": {"data": {"dt_added": 1467367588000, "uid": "08ced364c4584a1785fcc4d7ee9d14f7", "components": [{"order_rank": 1, "text": "para1", "comments": [{"text": "comment 1", "component_id": 1, "id": 1}, {"text": "comment 2", "component_id": 1, "id": 2}], "post_id": 1, "comp_type": 1, "id": 1, "dt_added": 1467367588000}, {"order_rank": 2, "text": "para2", "comments": [{"text": "comment 3", "component_id": 2, "id": 3}], "post_id": 1, "comp_type": 1, "id": 2, "dt_added": 1467367588000}, {"order_rank": 3, "text": "para3", "post_id": 1, "comp_type": 1, "id": 3, "dt_added": 1467367588000}], "title": "post 1"}}, "error": 0}
```

Comments can also be fetched separately for the post. See next section.

#### Getting comments
```
curl -i  localhost:8001/posts/08ced364c4584a1785fcc4d7ee9d14f7/comments/

HTTP/1.0 200 OK
Date: Fri, 01 Jul 2016 10:15:43 GMT
Server: WSGIServer/0.1 Python/2.7.6
X-Frame-Options: SAMEORIGIN
Content-Type: application/json

{"message": "", "result": {"data": [{"text": "comment 1", "component_id": 1, "id": 1}, {"text": "comment 2", "component_id": 1, "id": 2}, {"text": "comment 3", "component_id": 2, "id": 3}]}, "error": 0}
```

