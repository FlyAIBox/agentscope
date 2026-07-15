import { useState, useEffect, useCallback } from 'react';

import { credentialApi, modelApi } from '@/api';
import type { CredentialRecord, ModelCard } from '@/api';

export interface CredentialWithModels {
	credential: CredentialRecord;
	models: ModelCard[];
}

/**
 * Fetches all credentials and their available models, grouped by provider type.
 * Provider type is read from `credential.data.type`.
 * Model lists are resolved from each credential payload so OpenAI-compatible
 * base URLs can return their actual model IDs instead of the built-in defaults.
 */
export function useAvailableModels() {
	const [groups, setGroups] = useState<Record<string, CredentialWithModels[]>>({});
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<Error | null>(null);

	const refetch = useCallback(async () => {
		setLoading(true);
		setError(null);
		try {
			const { credentials } = await credentialApi.list();
			const result: Record<string, CredentialWithModels[]> = {};

			await Promise.all(
				credentials.map(async (credential) => {
					const type = credential.data.type as string | undefined;
					if (!type) return;
					if (!result[type]) result[type] = [];
					try {
						const { models } = await modelApi.listFromCredential(credential.data);
						result[type].push({ credential, models });
					} catch {
						try {
							const { models } = await modelApi.list(type);
							result[type].push({ credential, models });
						} catch {
							result[type].push({ credential, models: [] });
						}
					}
				}),
			);

			setGroups(result);
		} catch (e) {
			setError(e as Error);
		} finally {
			setLoading(false);
		}
	}, []);

	useEffect(() => {
		refetch();
	}, [refetch]);

	return { groups, loading, error, refetch };
}
