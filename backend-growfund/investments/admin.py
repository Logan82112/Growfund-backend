from django.contrib import admin
from django import forms
from .models import Trade, TradeHistory, CapitalInvestmentPlan


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'asset', 'trade_type', 'status', 'entry_price', 'quantity', 'profit_loss', 'created_at')
    list_filter = ('asset', 'trade_type', 'status', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'asset')
    readonly_fields = ('id', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Trade Information', {
            'fields': ('id', 'user', 'asset', 'trade_type', 'status')
        }),
        ('Pricing', {
            'fields': ('entry_price', 'current_price', 'exit_price', 'quantity')
        }),
        ('Risk Management', {
            'fields': ('stop_loss', 'take_profit', 'timeframe', 'expires_at')
        }),
        ('Performance', {
            'fields': ('profit_loss', 'profit_loss_percentage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'closed_at'),
            'description': 'Created date and closed date are editable for admin users. Changes will be tracked in the system.'
        }),
    )
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Override to make auto_now and auto_now_add fields editable"""
        if db_field.name == 'created_at':
            # Make created_at editable by removing auto_now_add behavior in admin
            kwargs['widget'] = forms.DateTimeInput(attrs={'type': 'datetime-local'})
            return forms.DateTimeField(**kwargs)
        elif db_field.name == 'updated_at':
            # Keep updated_at readonly
            pass
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('user')
    
    def get_readonly_fields(self, request, obj=None):
        """Allow date editing for trades"""
        readonly = ['id', 'updated_at']  # Always readonly
        
        # For existing trades, allow editing dates but keep other critical fields readonly
        if obj:
            readonly.extend(['user'])  # Keep user readonly for existing trades
        
        return readonly
    
    def save_model(self, request, obj, form, change):
        """Track changes made to trades"""
        if change:
            # Get the old trade to compare
            old_obj = Trade.objects.get(pk=obj.pk)
            
            # Track what was changed
            changes = []
            
            # Track date changes
            if old_obj.created_at != obj.created_at:
                changes.append(f"Created date changed from {old_obj.created_at.strftime('%Y-%m-%d %H:%M')} to {obj.created_at.strftime('%Y-%m-%d %H:%M')}")
            
            if old_obj.closed_at != obj.closed_at:
                old_closed = old_obj.closed_at.strftime('%Y-%m-%d %H:%M') if old_obj.closed_at else 'None'
                new_closed = obj.closed_at.strftime('%Y-%m-%d %H:%M') if obj.closed_at else 'None'
                changes.append(f"Closed date changed from {old_closed} to {new_closed}")
            
            # Log changes (you could add a notes field to the model if needed)
            if changes:
                print(f"Trade {obj.id} edited by admin {request.user.email}: {'; '.join(changes)}")
        
        super().save_model(request, obj, form, change)


@admin.register(TradeHistory)
class TradeHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'asset', 'trade_type', 'entry_price', 'exit_price', 'profit_loss', 'close_reason', 'closed_at')
    list_filter = ('asset', 'trade_type', 'close_reason', 'closed_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'asset')
    readonly_fields = ('id', 'closed_at')
    date_hierarchy = 'closed_at'
    
    fieldsets = (
        ('Trade Information', {
            'fields': ('id', 'user', 'asset', 'trade_type')
        }),
        ('Pricing', {
            'fields': ('entry_price', 'exit_price', 'quantity')
        }),
        ('Performance', {
            'fields': ('profit_loss', 'profit_loss_percentage')
        }),
        ('Details', {
            'fields': ('close_reason', 'opened_at', 'closed_at')
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('user')


@admin.register(CapitalInvestmentPlan)
class CapitalInvestmentPlanAdmin(admin.ModelAdmin):
    """Admin interface for Capital Investment Plans"""
    list_display = ('id', 'user', 'plan_type', 'initial_amount', 'growth_rate', 'period_months', 'final_amount', 'status', 'created_at')
    list_filter = ('plan_type', 'status', 'period_months', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('id', 'total_return', 'final_amount', 'monthly_growth', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Plan Information', {
            'fields': ('id', 'user', 'plan_type', 'status')
        }),
        ('Investment Details', {
            'fields': ('initial_amount', 'growth_rate', 'period_months')
        }),
        ('Calculated Returns', {
            'fields': ('total_return', 'final_amount', 'monthly_growth'),
            'description': 'These values are automatically calculated based on the growth rate and period.'
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'created_at', 'updated_at', 'completed_at'),
            'description': 'All dates are editable for admin users. Changes will be tracked in the system.'
        }),
    )
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Override to make auto_now and auto_now_add fields editable"""
        if db_field.name == 'created_at':
            # Make created_at editable by removing auto_now_add behavior in admin
            kwargs['widget'] = forms.DateTimeInput(attrs={'type': 'datetime-local'})
            return forms.DateTimeField(**kwargs)
        elif db_field.name == 'updated_at':
            # Keep updated_at readonly
            pass
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('user')
    
    def get_readonly_fields(self, request, obj=None):
        """Allow date editing for investment plans"""
        readonly = ['id', 'total_return', 'final_amount', 'monthly_growth', 'updated_at']  # Always readonly
        
        # For existing plans, allow editing dates but keep other critical fields readonly
        if obj:
            readonly.extend(['user'])  # Keep user readonly for existing plans
        
        return readonly
    
    def save_model(self, request, obj, form, change):
        """Track changes made to investment plans and recalculate if needed"""
        if change:
            # Get the old plan to compare
            old_obj = CapitalInvestmentPlan.objects.get(pk=obj.pk)
            
            # Track what was changed
            changes = []
            
            # Track date changes
            if old_obj.created_at != obj.created_at:
                changes.append(f"Created date changed from {old_obj.created_at.strftime('%Y-%m-%d %H:%M')} to {obj.created_at.strftime('%Y-%m-%d %H:%M')}")
            
            if old_obj.start_date != obj.start_date:
                changes.append(f"Start date changed from {old_obj.start_date.strftime('%Y-%m-%d %H:%M')} to {obj.start_date.strftime('%Y-%m-%d %H:%M')}")
            
            if old_obj.end_date != obj.end_date:
                old_end = old_obj.end_date.strftime('%Y-%m-%d %H:%M') if old_obj.end_date else 'None'
                new_end = obj.end_date.strftime('%Y-%m-%d %H:%M') if obj.end_date else 'None'
                changes.append(f"End date changed from {old_end} to {new_end}")
            
            if old_obj.completed_at != obj.completed_at:
                old_completed = old_obj.completed_at.strftime('%Y-%m-%d %H:%M') if old_obj.completed_at else 'None'
                new_completed = obj.completed_at.strftime('%Y-%m-%d %H:%M') if obj.completed_at else 'None'
                changes.append(f"Completed date changed from {old_completed} to {new_completed}")
            
            # Log changes
            if changes:
                print(f"Investment Plan {obj.id} edited by admin {request.user.email}: {'; '.join(changes)}")
        
        super().save_model(request, obj, form, change)
    
    actions = ['recalculate_returns', 'mark_completed']
    
    def recalculate_returns(self, request, queryset):
        """Recalculate returns for selected plans"""
        count = 0
        for plan in queryset:
            plan.calculate_returns()
            plan.save()
            count += 1
        self.message_user(request, f'Recalculated returns for {count} investment plans.')
    recalculate_returns.short_description = 'Recalculate returns for selected plans'
    
    def mark_completed(self, request, queryset):
        """Mark selected plans as completed"""
        from django.utils import timezone
        count = queryset.filter(status='active').update(
            status='completed',
            completed_at=timezone.now()
        )
        self.message_user(request, f'Marked {count} plans as completed.')
    mark_completed.short_description = 'Mark selected plans as completed'


# Admin Crypto Price Management
from .admin_models import AdminCryptoPrice, CryptoPriceHistory


@admin.register(AdminCryptoPrice)
class AdminCryptoPriceAdmin(admin.ModelAdmin):
    """Admin interface for crypto price management"""
    list_display = ('coin', 'name', 'buy_price', 'sell_price', 'spread_display', 'spread_pct_display', 'is_active', 'last_updated', 'updated_by')
    list_filter = ('is_active', 'last_updated')
    search_fields = ('coin', 'name')
    readonly_fields = ('spread_display', 'spread_pct_display', 'last_updated', 'created_at')
    
    fieldsets = (
        ('Coin Information', {
            'fields': ('coin', 'name', 'is_active')
        }),
        ('Pricing', {
            'fields': ('buy_price', 'sell_price', 'spread_display', 'spread_pct_display')
        }),
        ('Market Data', {
            'fields': ('change_24h', 'change_7d', 'change_30d')
        }),
        ('Metadata', {
            'fields': ('updated_by', 'last_updated', 'created_at')
        }),
    )
    
    def spread_display(self, obj):
        return f"${obj.spread:.2f}"
    spread_display.short_description = 'Spread'
    
    def spread_pct_display(self, obj):
        return f"{obj.spread_percentage:.2f}%"
    spread_pct_display.short_description = 'Spread %'
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(CryptoPriceHistory)
class CryptoPriceHistoryAdmin(admin.ModelAdmin):
    """Admin interface for price history"""
    list_display = ('coin', 'buy_price', 'sell_price', 'change_24h', 'updated_by', 'created_at')
    list_filter = ('coin', 'created_at')
    search_fields = ('coin',)
    readonly_fields = ('coin', 'buy_price', 'sell_price', 'change_24h', 'updated_by', 'created_at')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False  # History is auto-created
    
    def has_change_permission(self, request, obj=None):
        return False  # History cannot be modified