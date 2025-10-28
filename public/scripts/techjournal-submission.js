function initTechjournalSubmission(initialConfig) {
	let config = initialConfig ?? { enabled: false };

	if (!initialConfig) {
		const configEl = document.getElementById('techjournal-config');
		if (configEl?.textContent?.trim()) {
			try {
				config = JSON.parse(configEl.textContent);
			} catch (error) {
				console.warn('Failed to parse techjournal config', error);
			}
		}
	}

	const ackModal = document.getElementById('acknowledgement-modal');
	const mainContent = document.getElementById('main-content');
	const acceptButton = document.getElementById('accept-button');
	const addMeButton = document.getElementById('add-me-btn');
	const addTechjournalBtn = document.getElementById('add-techjournal-btn');
	const techjournalModal = document.getElementById('techjournal-modal');
	const cancelTechjournalBtn = document.getElementById('cancel-techjournal');
	const techjournalForm = document.getElementById('techjournal-form');
	const statusMessage = document.getElementById('techjournal-status');
	const submitButton = techjournalForm?.querySelector('button[type=\"submit\"]');
	const roleSelect = techjournalForm?.querySelector('#role-select');
	const gradYearGroup = techjournalForm?.querySelector('#grad-year-group');
	const gradYearInput = techjournalForm?.querySelector('#grad-year-input');
	const setFormInputsDisabled = (disabled) => {
		if (!techjournalForm) return;
		const interactiveFields = techjournalForm.querySelectorAll('input, select, textarea');
		interactiveFields.forEach((field) => {
			field.disabled = disabled;
		});
	};

	if (
		!ackModal ||
		!mainContent ||
		!acceptButton ||
		!addMeButton ||
		!addTechjournalBtn ||
		!techjournalModal ||
		!cancelTechjournalBtn ||
		!techjournalForm
	) {
		return;
	}

	const setStatus = (message, variant = 'pending') => {
		if (!statusMessage) return;
		statusMessage.textContent = message;
		statusMessage.classList.remove('status-success', 'status-error');
		if (variant === 'success') statusMessage.classList.add('status-success');
		if (variant === 'error') statusMessage.classList.add('status-error');
	};

	const toggleGradYear = () => {
		if (!roleSelect || !gradYearGroup || !gradYearInput) return;
		if (roleSelect.value === 'student') {
			gradYearGroup.classList.remove('hidden');
			gradYearInput.required = true;
		} else {
			gradYearGroup.classList.add('hidden');
			gradYearInput.required = false;
			gradYearInput.value = '';
		}
	};

	const resetRoleAndGradYear = () => {
		if (roleSelect) {
			roleSelect.value = '';
		}
		if (gradYearInput) {
			gradYearInput.value = '';
			gradYearInput.required = false;
		}
		if (gradYearGroup) {
			gradYearGroup.classList.add('hidden');
		}
	};

	const showMainContent = () => {
		ackModal.classList.add('hidden');
		ackModal.setAttribute('aria-hidden', 'true');
		mainContent.classList.remove('hidden');
		mainContent.removeAttribute('aria-hidden');
	};

	const openTechjournalModal = () => {
		techjournalModal.classList.remove('hidden');
		techjournalModal.setAttribute('aria-hidden', 'false');
		resetRoleAndGradYear();
		setFormInputsDisabled(false);
		if (statusMessage) {
			statusMessage.textContent = '';
			statusMessage.classList.remove('status-success', 'status-error');
		}
		if (submitButton) {
			submitButton.classList.remove('hidden');
			submitButton.type = 'submit';
			submitButton.textContent = 'Submit';
			submitButton.disabled = !(config.enabled && config.proxyBase);
		}
		if (cancelTechjournalBtn) {
			cancelTechjournalBtn.textContent = 'Cancel';
			if (!cancelTechjournalBtn.classList.contains('modal-button--outline')) {
				cancelTechjournalBtn.classList.add('modal-button--outline');
			}
		}
	};

	const closeTechjournalModal = () => {
		techjournalModal.classList.add('hidden');
		techjournalModal.setAttribute('aria-hidden', 'true');
		techjournalForm.reset();
		resetRoleAndGradYear();
		setFormInputsDisabled(false);
		if (submitButton) {
			submitButton.classList.remove('hidden');
			submitButton.type = 'submit';
			submitButton.textContent = 'Submit';
		}
		if (cancelTechjournalBtn) {
			cancelTechjournalBtn.textContent = 'Cancel';
			if (!cancelTechjournalBtn.classList.contains('modal-button--outline')) {
				cancelTechjournalBtn.classList.add('modal-button--outline');
			}
		}
		if (statusMessage) {
			statusMessage.textContent = '';
			statusMessage.classList.remove('status-success', 'status-error');
		}
	};

	acceptButton.addEventListener('click', showMainContent);

	addMeButton.addEventListener('click', () => {
		showMainContent();
		requestAnimationFrame(() => {
			openTechjournalModal();
			if (!config.enabled || !config.proxyBase) {
				setStatus('Submissions are not enabled at this time.', 'error');
				if (submitButton) {
					submitButton.disabled = true;
					submitButton.textContent = 'Submit';
				}
			} else if (submitButton) {
				submitButton.disabled = false;
			}
		});
	});

	if (config.enabled) {
		addTechjournalBtn.addEventListener('click', () => {
			openTechjournalModal();
		});
	} else {
		addTechjournalBtn.disabled = true;
		addTechjournalBtn.textContent = 'Submissions unavailable';
		addTechjournalBtn.title = 'Issue submission requires server configuration.';
	}

	cancelTechjournalBtn.addEventListener('click', () => {
		closeTechjournalModal();
	});

	roleSelect?.addEventListener('change', toggleGradYear);

	techjournalForm.addEventListener('submit', async (event) => {
		event.preventDefault();
		if (!config.enabled || !config.proxyBase) {
			setStatus('Submissions are not enabled at this time.', 'error');
			return;
		}

		const formData = new FormData(techjournalForm);
		const name = String(formData.get('name') ?? '').trim();
		const link = String(formData.get('link') ?? '').trim();
		const role = String(formData.get('role') ?? '').trim();
		const gradYearRaw = String(formData.get('gradYear') ?? '').trim();

		if (!name || !link) {
			setStatus('Both name and link are required.', 'error');
			return;
		}

		if (!role || (role !== 'student' && role !== 'staff')) {
			setStatus('Please choose whether you are a student or staff.', 'error');
			return;
		}

		let gradYear = '';
		if (role === 'student') {
			if (!gradYearRaw) {
				setStatus('Please provide your graduation year.', 'error');
				return;
			}
			if (!/^\d{4}$/.test(gradYearRaw)) {
				setStatus('Graduation year should be four digits (e.g., 2026).', 'error');
				return;
			}
			gradYear = gradYearRaw;
		}

		const originalButtonLabel = submitButton?.textContent ?? 'Submit';
		if (submitButton) {
			submitButton.disabled = true;
			submitButton.textContent = 'Submitting…';
		}

		setStatus('Submitting your request…');

		const payload = { name, link, role, gradYear };

		try {
			const response = await fetch(`${config.proxyBase}/techjournal`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(payload)
			});

			if (!response.ok) {
				const errorText = await response.text().catch(() => '');
				throw new Error(errorText || `Request failed with status ${response.status}`);
			}

			const data = (await response.json().catch(() => ({}))) || {};
			const statusSegments = [];
			if (data.issueUrl) {
				statusSegments.push(`Track the issue: ${data.issueUrl}`);
			}
			if (data.mergeRequestUrl) {
				statusSegments.push(`Review the merge request: ${data.mergeRequestUrl}`);
			} else if (data.mergeRequestError) {
				statusSegments.push(`Merge request note: ${data.mergeRequestError}`);
				if (data.mergeRequestDetails) {
					statusSegments.push(`Details: ${data.mergeRequestDetails}`);
				}
			}
			if (typeof data.tableRowAdded === 'boolean') {
				statusSegments.push(
					data.tableRowAdded
						? 'Your entry was queued for the public list.'
						: 'Your link was already on the public list.'
				);
			}

			const successMessage = statusSegments.length
				? `Thanks! Your submission was sent. ${statusSegments.join(' ')}`
				: 'Thanks! Your submission was sent.';

			setStatus(successMessage, 'success');
			techjournalForm.reset();
			setFormInputsDisabled(true);
			if (submitButton) {
				submitButton.classList.add('hidden');
				submitButton.disabled = false;
			}
			if (cancelTechjournalBtn) {
				cancelTechjournalBtn.textContent = 'Done';
				cancelTechjournalBtn.classList.remove('modal-button--outline');
				cancelTechjournalBtn.focus();
			}
		} catch (error) {
			console.error('Unable to submit techjournal issue', error);
			setStatus('Something went wrong submitting your request. Please try again later.', 'error');
		} finally {
			if (submitButton) {
				submitButton.disabled = false;
				submitButton.textContent = originalButtonLabel;
			}
		}
	});

	document.addEventListener('keydown', (event) => {
		if (event.key === 'Escape' && !techjournalModal.classList.contains('hidden')) {
			closeTechjournalModal();
		}
	});
}

if (typeof window !== 'undefined') {
	const run = () => initTechjournalSubmission();
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', run, { once: true });
	} else {
		run();
	}
}

export { initTechjournalSubmission };
