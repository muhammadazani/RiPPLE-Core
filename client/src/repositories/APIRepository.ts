import "whatwg-fetch";
import Fetcher from "../services/Fetcher";

declare const process;
declare let fetch;

let token = undefined;

export const API = process.env.API_LOCATION;
export const NODE_ENV = process.env.NODE_ENV;

const mergeAuthHeader = (options: Object) => {
    if (options === undefined) {
        options = {};
    }

    if (options["headers"] === undefined) {
        options["headers"] = new Headers();
    }

    if (token !== undefined) {
        options["headers"].append("Authorization", token);
    };

    return options;
};

export const blobFetch = (url: string, options?: Object) => {
    return fetch(`${url}`, options)
        .then(response => {
            if (!response.ok) {
                throw response;
            }
            return response;
        });
};

export const apiFetch = <T>(url: string, opts?: Object): Promise<T> => {
    const options = mergeAuthHeader(opts);
    return fetch(`${API}${url}`, options)
        .then(response => {
            if (!response.ok) {
                throw response;
            }
            if (response.status >= 200 && response.status < 300) {
                if (response.status == 204) {
                    return Promise.resolve({});
                } else {
                    return response.json() as Promise<T>;
                }
            }
            // Fallthrough to error
            Promise.resolve({});
        })
        .then(serverResponse => {
            if (serverResponse.achievement) {
                // Do global things
                // Fetcher.forceUpdate(false);
            }
            return serverResponse;
        });
};

export const setToken = newToken => {
    token = newToken;
};
