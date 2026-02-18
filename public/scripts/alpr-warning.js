(() => {
	const noteElement =
		document.getElementById('alpr-note-hidden') || document.getElementById('alpr-note');
	const stateLabel = document.getElementById('alpr-state-label');
	const privacyLink = document.getElementById('alpr-privacy-link');
	const closeButton = document.getElementById('alpr-close-button');
	if (!noteElement || !stateLabel || !privacyLink || !closeButton) {
		return;
	}

	const cookieName = 'alpr-notice-shown';
	if (document.cookie.includes(cookieName)) {
		return;
	}

	let stateCodes = [];
	try {
		stateCodes = JSON.parse(noteElement.dataset.alprStates || '[]');
	} catch (error) {
		stateCodes = [];
	}

	if (!Array.isArray(stateCodes) || stateCodes.length === 0) {
		return;
	}

	const rawGeoipUrl = noteElement.dataset.geoipUrl || '';
	const geoipUrl = /^https?:\/\//i.test(rawGeoipUrl) ? rawGeoipUrl : 'https://ipapi.co/json/';
	const privacyLinkHref = noteElement.dataset.privacyLink || '/techopinions/privacy';

	const stateNameToCode = {
		alabama: 'AL',
		alaska: 'AK',
		arizona: 'AZ',
		arkansas: 'AR',
		california: 'CA',
		colorado: 'CO',
		connecticut: 'CT',
		delaware: 'DE',
		florida: 'FL',
		georgia: 'GA',
		hawaii: 'HI',
		idaho: 'ID',
		illinois: 'IL',
		indiana: 'IN',
		iowa: 'IA',
		kansas: 'KS',
		kentucky: 'KY',
		louisiana: 'LA',
		maine: 'ME',
		maryland: 'MD',
		massachusetts: 'MA',
		michigan: 'MI',
		minnesota: 'MN',
		mississippi: 'MS',
		missouri: 'MO',
		montana: 'MT',
		nebraska: 'NE',
		nevada: 'NV',
		'new hampshire': 'NH',
		'new jersey': 'NJ',
		'new mexico': 'NM',
		'new york': 'NY',
		'north carolina': 'NC',
		'north dakota': 'ND',
		ohio: 'OH',
		oklahoma: 'OK',
		oregon: 'OR',
		pennsylvania: 'PA',
		'rhode island': 'RI',
		'south carolina': 'SC',
		'south dakota': 'SD',
		tennessee: 'TN',
		texas: 'TX',
		utah: 'UT',
		vermont: 'VT',
		virginia: 'VA',
		washington: 'WA',
		'west virginia': 'WV',
		wisconsin: 'WI',
		wyoming: 'WY',
		'district of columbia': 'DC'
	};

	const normalizeStateCode = (value) => {
		if (!value) {
			return null;
		}
		const trimmed = value.trim();
		if (!trimmed) {
			return null;
		}
		const upper = trimmed.toUpperCase();
		if (upper.length === 2) {
			return upper;
		}
		return stateNameToCode[trimmed.toLowerCase()] || null;
	};

	const closeNotice = () => {
		noteElement.id = 'alpr-note-hidden';
		noteElement.setAttribute('aria-hidden', 'true');
		document.cookie = `${cookieName}=true;path=/;max-age=2592000`;
		document.removeEventListener('keydown', handleKeydown);
	};

	closeButton.addEventListener('click', closeNotice);
	noteElement.addEventListener('click', (event) => {
		if (event.target === noteElement) {
			closeNotice();
		}
	});

	const handleKeydown = (event) => {
		if (event.key === 'Escape') {
			closeNotice();
		}
	};

	const getRegionFromResponse = (data) => {
		if (!data || typeof data !== 'object') {
			return { code: null, label: null };
		}
		const regionCode =
			data.region_code || data.regionCode || data.region || data.region_name || data.state;
		const code = normalizeStateCode(String(regionCode || ''));
		const label = data.region || data.region_name || data.regionCode || data.state || code;
		return { code, label };
	};

	fetch(geoipUrl, { credentials: 'omit' })
		.then((response) => response.json())
		.then((data) => {
			const region = getRegionFromResponse(data);
			if (!region.code || !stateCodes.includes(region.code)) {
				return;
			}
			noteElement.id = 'alpr-note';
			noteElement.setAttribute('aria-hidden', 'false');
			stateLabel.textContent = region.label || region.code;
			privacyLink.setAttribute('href', privacyLinkHref);
			document.addEventListener('keydown', handleKeydown);
		})
		.catch(() => {
			// Ignore geo lookup failures.
		});
})();
