import { GetObjectCommand, S3Client } from "@aws-sdk/client-s3";
import { Context, Handler, S3Event } from "aws-lambda";
import { writeFileSync, promises as fsPromises } from "fs";
import path = require("path");

export const handler: Handler = async (event: S3Event, context: Context): Promise<any> => {
    const efsPath = process.env.EFS_PATH!;

    const s3Client = new S3Client({});

    await new Promise(function (resolve, reject) {
        event.Records.forEach(async (record) => {
            const bucketName = record.s3.bucket.name;
            // const key = record.s3.object.key.replace(/\+/g, " ");
            const key = record.s3.object.key;
            const params = {
                Bucket: bucketName,
                Key: key,
            };

            console.log(`Copying ${key} from ${bucketName} to ${efsPath}`)

            try {
                const data = await s3Client.send(new GetObjectCommand(params));
                // console.log("Data", data)

                if (data.Body != undefined) {
                    const bytes = await data.Body.transformToByteArray();
                    const filePath = path.join(efsPath, key);

                    console.log(`Writing data to ${filePath}`);

                    const directory = path.dirname(filePath);
                    console.log(`Creating directory ${directory}`);

                    try {
                        await fsPromises.mkdir(directory, { recursive: true });
                    } catch (mkdirErr) {
                        if (mkdirErr instanceof Error) {
                            const err = mkdirErr as NodeJS.ErrnoException;
                            if (err.code !== 'EEXIST') {
                                throw err;
                            }
                        } else {
                            throw mkdirErr;
                        }
                    }

                    // Ahora debería ser seguro escribir el archivo
                    await fsPromises.writeFile(filePath, Buffer.from(bytes));
                    console.log(`Successfully uploaded data to ${filePath}`);

                    console.log(`Successfully uploaded data to ${efsPath}/${key}`)
                } else {
                    console.log("Body is undefined");
                }
            } catch (err) {
                console.log(err);
                reject(err);
            }
        });
    });
};