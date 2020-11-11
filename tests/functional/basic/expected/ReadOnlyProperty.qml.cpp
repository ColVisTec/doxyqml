/**
 * An item with readonly properties
 */
class ReadOnlyProperty : public QtQuick.Item {
public:
/**
     * A readonly property
     */
/** @remark This property is read-only */
Q_PROPERTY(real gravity READ dummyGetter_gravity_ignore)
/**
     * A read-write property
     */
Q_PROPERTY(real speed READ dummyGetter_speed_ignore)
};
