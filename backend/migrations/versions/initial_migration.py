from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('robot_devices',
        sa.Column('device_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('device_name', sa.String(), nullable=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('device_id')
    )
    op.create_table('telemetry_metrics',
        sa.Column('metric_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('metric_name', sa.String(), nullable=False),
        sa.Column('metric_unit', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('metric_id'),
        sa.UniqueConstraint('metric_name')
    )
    op.create_table('telemetry_data',
        sa.Column('data_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('device_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('metric_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('value', sa.String(), nullable=False),
        sa.Column('recorded_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['robot_devices.device_id']),
        sa.ForeignKeyConstraint(['metric_id'], ['telemetry_metrics.metric_id']),
        sa.PrimaryKeyConstraint('data_id')
    )
    op.create_table('command_logs',
        sa.Column('command_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('device_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('command', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['robot_devices.device_id']),
        sa.PrimaryKeyConstraint('command_id')
    )
    op.execute("INSERT INTO telemetry_metrics (metric_id, metric_name, metric_unit) VALUES (gen_random_uuid(), 'play_sessions', 'count')")
    op.execute("INSERT INTO telemetry_metrics (metric_id, metric_name, metric_unit) VALUES (gen_random_uuid(), 'feeding_times', 'count')")
    op.execute("INSERT INTO telemetry_metrics (metric_id, metric_name, metric_unit) VALUES (gen_random_uuid(), 'feed_dispensed', 'grams')")
    op.execute("INSERT INTO telemetry_metrics (metric_id, metric_name, metric_unit) VALUES (gen_random_uuid(), 'task_count', 'count')")
    op.execute("INSERT INTO telemetry_metrics (metric_id, metric_name, metric_unit) VALUES (gen_random_uuid(), 'battery_level', '%')")
    op.execute("INSERT INTO telemetry_metrics (metric_id, metric_name, metric_unit) VALUES (gen_random_uuid(), 'temperature', '°C')")
    op.execute("INSERT INTO telemetry_metrics (metric_id, metric_name, metric_unit) VALUES (gen_random_uuid(), 'activity_duration', 'minutes')")
    op.execute("INSERT INTO telemetry_metrics (metric_id, metric_name, metric_unit) VALUES (gen_random_uuid(), 'health_alerts', 'count')")
    op.execute("INSERT INTO telemetry_metrics (metric_id, metric_name, metric_unit) VALUES (gen_random_uuid(), 'camera_usage', 'count')")
    op.execute("INSERT INTO telemetry_metrics (metric_id, metric_name, metric_unit) VALUES (gen_random_uuid(), 'training_sessions', 'count')")

def downgrade():
    op.drop_table('command_logs')
    op.drop_table('telemetry_data')
    op.drop_table('telemetry_metrics')
    op.drop_table('robot_devices')
