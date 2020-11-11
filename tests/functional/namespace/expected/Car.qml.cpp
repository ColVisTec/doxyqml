namespace ns {
/**
 * A car
 */
class Car : public QtQuick.Item {
public:
/**
     * Car speed
     */
Q_PROPERTY(real speed READ dummyGetter_speed_ignore)
};
}
