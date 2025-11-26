from flask import Blueprint, request, jsonify
from supabase_client import get_supabase
import uuid
from datetime import datetime

api = Blueprint('api', __name__, url_prefix='/api')
supabase = get_supabase()

@api.route('/events', methods=['POST'])
def create_event():
    try:
        data = request.get_json()
        result = supabase.table('events').insert({
            'title': data.get('title'),
            'date': data.get('date'),
            'time': data.get('time'),
            'location': data.get('location', ''),
            'description': data.get('description', ''),
            'host': data.get('host', ''),
            'template': data.get('template', 'modern'),
            'custom_template': data.get('customTemplate'),
            'rsvp_deadline': data.get('rsvpDeadline'),
            'dress_code': data.get('dressCode', '')
        }).execute()
        return jsonify({'success': True, 'data': result.data[0]}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/events', methods=['GET'])
def get_events():
    try:
        result = supabase.table('events').select('*').order('created_at', desc=True).execute()
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    try:
        result = supabase.table('events').select('*').eq('id', event_id).single().execute()
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    try:
        data = request.get_json()
        data['updated_at'] = datetime.now().isoformat()
        result = supabase.table('events').update(data).eq('id', event_id).execute()
        return jsonify({'success': True, 'data': result.data[0]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        supabase.table('events').delete().eq('id', event_id).execute()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/contacts', methods=['POST'])
def create_contact():
    try:
        data = request.get_json()
        result = supabase.table('contacts').insert({
            'name': data.get('name'),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'group': data.get('group', 'Friends'),
            'preferences': data.get('preferences', {})
        }).execute()
        return jsonify({'success': True, 'data': result.data[0]}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/contacts', methods=['GET'])
def get_contacts():
    try:
        result = supabase.table('contacts').select('*').order('name').execute()
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/contacts/<contact_id>', methods=['PUT'])
def update_contact(contact_id):
    try:
        data = request.get_json()
        data['updated_at'] = datetime.now().isoformat()
        result = supabase.table('contacts').update(data).eq('id', contact_id).execute()
        return jsonify({'success': True, 'data': result.data[0]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    try:
        supabase.table('contacts').delete().eq('id', contact_id).execute()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/contacts/bulk', methods=['POST'])
def bulk_create_contacts():
    try:
        data = request.get_json()
        contacts = data.get('contacts', [])
        result = supabase.table('contacts').insert(contacts).execute()
        return jsonify({'success': True, 'data': result.data}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/voice-samples', methods=['POST'])
def create_voice_sample():
    try:
        data = request.get_json()
        result = supabase.table('voice_samples').insert({
            'name': data.get('name'),
            'audio_url': data.get('audioUrl'),
            'duration': data.get('duration', 0),
            'status': data.get('status', 'recorded'),
            'metadata': data.get('metadata', {})
        }).execute()
        return jsonify({'success': True, 'data': result.data[0]}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/voice-samples', methods=['GET'])
def get_voice_samples():
    try:
        result = supabase.table('voice_samples').select('*').order('created_at', desc=True).execute()
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/voice-samples/<sample_id>', methods=['DELETE'])
def delete_voice_sample(sample_id):
    try:
        supabase.table('voice_samples').delete().eq('id', sample_id).execute()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/invitations', methods=['POST'])
def create_invitation():
    try:
        data = request.get_json()
        tracking_token = str(uuid.uuid4())
        result = supabase.table('invitations').insert({
            'event_id': data.get('eventId'),
            'contact_id': data.get('contactId'),
            'status': data.get('status', 'pending'),
            'delivery_method': data.get('deliveryMethod', 'email'),
            'sent_at': datetime.now().isoformat(),
            'tracking_token': tracking_token,
            'voice_message_url': data.get('voiceMessageUrl'),
            'metadata': data.get('metadata', {})
        }).execute()
        return jsonify({'success': True, 'data': result.data[0]}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/invitations', methods=['GET'])
def get_invitations():
    try:
        event_id = request.args.get('event_id')
        query = supabase.table('invitations').select('*, events(*), contacts(*)')
        if event_id:
            query = query.eq('event_id', event_id)
        result = query.order('created_at', desc=True).execute()
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/invitations/<invitation_id>', methods=['PUT'])
def update_invitation(invitation_id):
    try:
        data = request.get_json()
        if data.get('status') and not data.get('responded_at'):
            data['responded_at'] = datetime.now().isoformat()
        result = supabase.table('invitations').update(data).eq('id', invitation_id).execute()
        return jsonify({'success': True, 'data': result.data[0]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/invitations/track/<tracking_token>', methods=['POST'])
def track_invitation(tracking_token):
    try:
        action = request.get_json().get('action')
        update_data = {}
        if action == 'opened':
            update_data['opened_at'] = datetime.now().isoformat()
        result = supabase.table('invitations').update(update_data).eq('tracking_token', tracking_token).execute()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/invitations/bulk-send', methods=['POST'])
def bulk_send_invitations():
    try:
        data = request.get_json()
        event_id = data.get('eventId')
        contact_ids = data.get('contactIds', [])
        delivery_method = data.get('deliveryMethod', 'email')
        voice_url = data.get('voiceMessageUrl')

        invitations = []
        for contact_id in contact_ids:
            invitations.append({
                'event_id': event_id,
                'contact_id': contact_id,
                'status': 'pending',
                'delivery_method': delivery_method,
                'sent_at': datetime.now().isoformat(),
                'tracking_token': str(uuid.uuid4()),
                'voice_message_url': voice_url
            })

        result = supabase.table('invitations').insert(invitations).execute()
        return jsonify({'success': True, 'data': result.data}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/custom-templates', methods=['POST'])
def create_template():
    try:
        data = request.get_json()
        result = supabase.table('custom_templates').insert({
            'name': data.get('name'),
            'html_content': data.get('htmlContent'),
            'preview_image': data.get('previewImage'),
            'is_public': data.get('isPublic', False)
        }).execute()
        return jsonify({'success': True, 'data': result.data[0]}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/custom-templates', methods=['GET'])
def get_templates():
    try:
        result = supabase.table('custom_templates').select('*').order('created_at', desc=True).execute()
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api.route('/stats', methods=['GET'])
def get_stats():
    try:
        event_id = request.args.get('event_id')

        contacts_result = supabase.table('contacts').select('*', count='exact').execute()
        events_result = supabase.table('events').select('*', count='exact').execute()

        query = supabase.table('invitations').select('*')
        if event_id:
            query = query.eq('event_id', event_id)
        invitations_result = query.execute()

        invitations = invitations_result.data
        stats = {
            'total_contacts': contacts_result.count,
            'total_events': events_result.count,
            'total_invitations': len(invitations),
            'accepted': len([i for i in invitations if i['status'] == 'accepted']),
            'declined': len([i for i in invitations if i['status'] == 'declined']),
            'pending': len([i for i in invitations if i['status'] == 'pending']),
            'maybe': len([i for i in invitations if i['status'] == 'maybe'])
        }

        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
