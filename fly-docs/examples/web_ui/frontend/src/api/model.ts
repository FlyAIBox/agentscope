import { client } from './client';
import type { ListModelResponse, ListTTSModelResponse } from './types';

export const modelApi = {
	list: (provider: string) => client.get<ListModelResponse>('/model/', { provider }),

	listFromCredential: (data: Record<string, unknown>) =>
		client.post<ListModelResponse>(
			'/model/from-credential',
			{ data },
			undefined,
			{ silent: true },
		),
};

export const ttsModelApi = {
	list: (provider: string) => client.get<ListTTSModelResponse>('/tts-model/', { provider }),
};
