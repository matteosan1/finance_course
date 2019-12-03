#! /bin/bash

echo "USERNAME: $GITLAB_USER_LOGIN"
echo "ASSIGNEE: $CI_MERGE_REQUEST_ASSIGNEES"

if [[ "$GITLAB_USER_LOGIN" == "$CI_MERGE_REQUEST_ASSIGNEES" ]]
then
    echo "An assignee cannot approve its own merge requests..."
    exit 255
fi
