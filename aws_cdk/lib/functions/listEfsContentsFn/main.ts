import { Handler } from "aws-lambda";
import { readdirSync, statSync, Dirent } from "fs";

const getAllFilesAndDirectories = (dirPath: string): string[] => {
    const entries: Dirent[] = readdirSync(dirPath, { withFileTypes: true });
    const filesAndDirectories: string[] = [];

    for (const entry of entries) {
        const fullPath = `${dirPath}/${entry.name}`;
        filesAndDirectories.push(fullPath);

        if (entry.isDirectory()) {
            filesAndDirectories.push(...getAllFilesAndDirectories(fullPath));
        }
    }

    return filesAndDirectories;
};

export const handler: Handler = async (event, context) => {
    const efsPath = process.env.EFS_PATH!;

    try {
        const allFilesAndDirectories = getAllFilesAndDirectories(efsPath);

        return {
            statusCode: 200,
            body: JSON.stringify(`Files and Directories (${efsPath}): ${allFilesAndDirectories.join(", ")}`),
        };
    } catch (error: any) {
        return {
            statusCode: 500,
            body: JSON.stringify(`Error: ${error.message}`),
        };
    }
};
