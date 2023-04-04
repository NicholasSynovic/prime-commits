from json import loads

schemaStr: str = """{
    "$schema": "http://json-schema.org/draft-06/schema#",
    "type": "object",
    "additionalProperties": {
        "$ref": "#/definitions/CommitInformation"
    },
    "definitions": {
        "CommitInformation": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "id": {
                    "type": "string"
                },
                "CommitDate": {
                    "type": "integer"
                },
                "CommitMessage": {
                    "type": "string"
                },
                "AuthorName": {
                    "type": "string"
                },
                "AuthorEmail": {
                    "type": "string"
                },
                "AuthorDate": {
                    "type": "integer"
                },
                "CommiterName": {
                    "type": "string"
                },
                "CommiterEmail": {
                    "type": "string"
                },
                "CommiterDate": {
                    "type": "integer"
                },
                "CommitDaysSince0": {
                    "type": "integer"
                },
                "CommiterDaysSince0": {
                    "type": "integer"
                },
                "AuthorDaysSince0": {
                    "type": "integer"
                },
                "NumberOfFiles": {
                    "type": "integer"
                },
                "NumberOfLines": {
                    "type": "integer"
                },
                "NumberOfBlankLines": {
                    "type": "integer"
                },
                "NumberOfCommentLines": {
                    "type": "integer"
                },
                "LOC": {
                    "type": "integer"
                },
                "KLOC": {
                    "type": "number"
                },
                "SCC_Complexity": {
                    "type": "integer"
                },
                "Bytes": {
                    "type": "integer"
                },
                "DLOC": {
                    "type": "integer"
                },
                "DKLOC": {
                    "type": "number"
                }
            },
            "required": [
                "AuthorDate",
                "AuthorDaysSince0",
                "AuthorEmail",
                "AuthorName",
                "Bytes",
                "CommitDate",
                "CommitDaysSince0",
                "CommitMessage",
                "CommiterDate",
                "CommiterDaysSince0",
                "CommiterEmail",
                "CommiterName",
                "DKLOC",
                "DLOC",
                "KLOC",
                "LOC",
                "NumberOfBlankLines",
                "NumberOfCommentLines",
                "NumberOfFiles",
                "NumberOfLines",
                "SCC_Complexity",
                "id"
            ],
            "title": "CommitInformation"
        }
    }
}
"""

schema: dict = loads(s=schemaStr)
