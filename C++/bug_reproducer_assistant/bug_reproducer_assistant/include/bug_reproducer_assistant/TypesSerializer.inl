//Boost
#include <boost/make_shared.hpp>
//Json
#include <json/value.h>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/Json_specific.h>

namespace bug_reproducer_assistant
{

inline std::string TypesSerializer::getJsonNullValue()
{
	Json::Value val(Json::nullValue);
	return getStringFromJson(val);
}

inline std::string TypesSerializer::getJsonIntValue(const int* i)
{
	Json::Value val = *i;
	return getStringFromJson(val);
}

inline std::string TypesSerializer::getJsonUIntValue(const unsigned int* u)
{
	Json::Value val = *u;
	return getStringFromJson(val);
}

inline std::string TypesSerializer::getJsonDoubleValue(const double* d)
{
	Json::Value val = *d;
	return getStringFromJson(val);
}

inline std::string TypesSerializer::getJsonStringValue(const std::string* str)
{
	Json::Value val = *str;
	return getStringFromJson(val);
}

template < class T >
std::string TypesSerializer::getJsonArrayValue(const std::vector<T>* v)
{
	//Only vector for primitive types
	Json::Value val(Json::arrayValue);
	for( std::vector<T>::const_iterator it = v->begin(); it != v->end(); ++it )
	{
		Json::Value elemVal = *it;
		val.append(elemVal);
	}
	return getStringFromJson(val);
}

template < class Key, class Value >    
std::string TypesSerializer::getJsonObjectValue(const std::map< Key, Value >* m )
{
	//Only map for primitive types
	Json::Value val(Json::objectValue);
	for( std::map<Key, Value>::const_iterator it = m->begin(); it != m->end(); ++it )
		val[it->first] = it->second;
	return getStringFromJson(val);
}

} // namespace bug_reproducer_assistant