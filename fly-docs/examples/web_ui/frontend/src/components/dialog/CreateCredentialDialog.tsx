import { CircleAlert, Loader2, PlusCircle } from 'lucide-react';
import { useState, useEffect } from 'react';

import { credentialApi } from '@/api';
import type { CredentialSchema } from '@/api';
import {
	SchemaForm,
	defaultValuesFromSchema,
	type SchemaFormValue,
} from '@/components/form/SchemaForm';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import {
	Dialog,
	DialogContent,
	DialogHeader,
	DialogTitle,
	DialogDescription,
	DialogFooter,
} from '@/components/ui/dialog';
import { Field, FieldGroup, FieldLabel } from '@/components/ui/field.tsx';
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from '@/components/ui/select';
import { useCredentials } from '@/hooks/useCredentials';
import { useTranslation } from '@/i18n/useI18n.ts';

interface Props {
	open: boolean;
	onOpenChange: (open: boolean) => void;
	onCreated?: () => void;
	defaultType?: string;
}

export function CreateCredentialDialog({ open, onOpenChange, onCreated, defaultType }: Props) {
	const { create } = useCredentials();
	const { t } = useTranslation();
	const [schemas, setSchemas] = useState<CredentialSchema[]>([]);
	const [loadingSchemas, setLoadingSchemas] = useState(false);
	const [selectedType, setSelectedType] = useState('');
	const [values, setValues] = useState<Record<string, SchemaFormValue>>({});
	const [submitting, setSubmitting] = useState(false);
	const [testing, setTesting] = useState(false);
	const [testResult, setTestResult] = useState<{
		type: 'success' | 'error';
		message: string;
	} | null>(null);

	useEffect(() => {
		if (!open) return;
		setLoadingSchemas(true);
		credentialApi
			.schemas()
			.then((res) => {
				setSchemas(res.schemas);
				if (res.schemas.length > 0) {
					const first = (res.schemas[0].properties.type?.const as string) ?? '';
					const nextType = defaultType ?? first;
					const nextSchema = res.schemas.find(
						(s) => (s.properties.type?.const as string) === nextType,
					);
					setSelectedType(nextType);
					setValues(nextSchema ? defaultValuesFromSchema(nextSchema) : {});
					setTestResult(null);
				}
			})
			.finally(() => setLoadingSchemas(false));
	}, [open, defaultType]);

	const selectedSchema = schemas.find(
		(s) => (s.properties.type?.const as string) === selectedType,
	);

	const handleTypeChange = (type: string) => {
		setSelectedType(type);
		const nextSchema = schemas.find((s) => (s.properties.type?.const as string) === type);
		setValues(nextSchema ? defaultValuesFromSchema(nextSchema) : {});
		setTestResult(null);
	};

	const buildData = () => {
		if (!selectedSchema) return;
		const data: Record<string, unknown> = { type: selectedType };
		for (const [key, prop] of Object.entries(selectedSchema.properties)) {
			if (key === 'id' || key === 'type' || prop.const !== undefined) continue;
			const val = values[key];
			if (val !== undefined && val !== '') data[key] = val;
		}
		return data;
	};

	const handleTest = async () => {
		const data = buildData();
		if (!data) return;
		setTesting(true);
		setTestResult(null);
		try {
			const res = await credentialApi.test({ data });
			setTestResult({ type: 'success', message: res.message });
		} catch (e) {
			setTestResult({
				type: 'error',
				message: e instanceof Error ? e.message : t('dialog-credential-create.testFailed'),
			});
		} finally {
			setTesting(false);
		}
	};

	const handleSubmit = async () => {
		const data = buildData();
		if (!data) return;
		setSubmitting(true);
		try {
			await create({ data });
			onOpenChange(false);
			onCreated?.();
		} finally {
			setSubmitting(false);
		}
	};

	return (
		<Dialog open={open} onOpenChange={onOpenChange}>
			<DialogContent className="!w-[500px] !max-w-[500px]">
				<DialogHeader>
					<DialogTitle>{t('dialog-credential-create.title')}</DialogTitle>
					<DialogDescription>
						{t('dialog-credential-create.description')}
					</DialogDescription>
				</DialogHeader>
				<FieldGroup>
					<Field>
						<FieldLabel>{t('dialog-credential-create.selectType')}</FieldLabel>
						<Select
							value={selectedType}
							onValueChange={handleTypeChange}
							disabled={loadingSchemas}
						>
							<SelectTrigger>
								<SelectValue
									placeholder={
										loadingSchemas
											? t('common.loading')
											: t('dialog-credential-create.selectTypePlaceholder')
									}
								/>
							</SelectTrigger>
							<SelectContent>
								{schemas.map((s) => (
									<SelectItem
										key={s.properties.type?.const as string}
										value={s.properties.type?.const as string}
									>
										{s.title}
									</SelectItem>
								))}
							</SelectContent>
						</Select>
					</Field>
					{selectedSchema && (
						<SchemaForm
							schema={selectedSchema}
							values={values}
							onChange={(key, val) => {
								setValues((prev) => ({ ...prev, [key]: val }));
								setTestResult(null);
							}}
						/>
					)}
				</FieldGroup>
				{testResult && (
					<Alert variant={testResult.type === 'error' ? 'destructive' : 'default'}>
						<AlertDescription>{testResult.message}</AlertDescription>
					</Alert>
				)}
				<DialogFooter>
					<Button
						variant="outline"
						onClick={handleTest}
						disabled={testing || submitting || !selectedSchema}
					>
						{testing && <Loader2 className="size-3.5 animate-spin" />}
						{testing
							? t('dialog-credential-create.testing')
							: t('dialog-credential-create.test')}
					</Button>
					<Button
						variant="ghost"
						onClick={() => onOpenChange(false)}
						disabled={submitting || testing}
					>
						<CircleAlert className="size-3.5" />
						{t('common.cancel')}
					</Button>
					<Button onClick={handleSubmit} disabled={submitting || testing || !selectedSchema}>
						{submitting ? (
							<Loader2 className="size-3.5 animate-spin" />
						) : (
							<PlusCircle className="size-3.5" />
						)}
						{submitting ? t('common.creating') : t('common.create')}
					</Button>
				</DialogFooter>
			</DialogContent>
		</Dialog>
	);
}
