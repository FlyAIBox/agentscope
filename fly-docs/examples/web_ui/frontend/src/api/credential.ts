import { client } from './client';
import type {
	CreateCredentialRequest,
	CreateCredentialResponse,
	CredentialListResponse,
	CredentialRecord,
	CredentialSchemasResponse,
	CredentialTestResponse,
	UpdateCredentialRequest,
} from './types';

export const credentialApi = {
	list: () => client.get<CredentialListResponse>('/credential/'),

	schemas: () => client.get<CredentialSchemasResponse>('/credential/schemas'),

	create: (body: CreateCredentialRequest) =>
		client.post<CreateCredentialResponse>('/credential/', body),

	update: (credentialId: string, body: UpdateCredentialRequest) =>
		client.patch<CredentialRecord>(`/credential/${credentialId}`, body),

	test: (body: CreateCredentialRequest) =>
		client.post<CredentialTestResponse>('/credential/test', body, undefined, {
			silent: true,
		}),

	delete: (credentialId: string) => client.delete(`/credential/${credentialId}`),
};
